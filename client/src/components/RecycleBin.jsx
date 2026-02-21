import { useEffect, useState, useCallback } from 'react';
import '../styles/recycle-bin.css';
import axios from 'axios';

const URL_SERVER = {
    binInfo: "http://localhost:5000/api/binInfo",
    getInfoFiles: "http://localhost:5000/api/getInfoFiles",
    empty: "http://localhost:5000/api/empty",
    restore: "http://localhost:5000/api/restore"
};

/* ── File item inside the popup ── */
const FileItem = ({ name, path, onRestore, restoring }) => (
    <div className="rb-file-item">
        <div className="rb-file-icon">📄</div>
        <div className="rb-file-info">
            <span className="rb-file-name" title={name}>{name}</span>
            <span className="rb-file-path" title={path}>{path}</span>
        </div>
        <button
            className="rb-btn-restore"
            onClick={onRestore}
            disabled={restoring}
            title="Restaurar archivo"
        >
            ↩️
        </button>
    </div>
);

/* ── Empty state ── */
const EmptyState = () => (
    <div className="rb-empty-state">
        <span className="rb-empty-icon">🗑️</span>
        <p>La papelera está vacía</p>
    </div>
);

/* ── Popup panel ── */
const RecycleBinPopup = ({ isOpen, files, onClose, onRestore, onEmpty, loading, restoringIdx }) => (
    <>
        {/* Overlay */}
        <div className={`rb-overlay${isOpen ? ' active' : ''}`} onClick={onClose} />

        {/* Panel */}
        <div className={`rb-popup${isOpen ? ' active' : ''}`}>
            {/* Header */}
            <div className="rb-popup-header">
                <h2 className="rb-popup-title">🗑️ Papelera de Reciclaje</h2>
                <button className="rb-btn-close" onClick={onClose}>✕</button>
            </div>

            {/* Divider */}
            <div className="rb-divider" />

            {/* Body */}
            <div className="rb-popup-body">
                {loading ? (
                    <div className="rb-loading">
                        <div className="rb-spinner" />
                        <p>Cargando archivos…</p>
                    </div>
                ) : files.length === 0 ? (
                    <EmptyState />
                ) : (
                    files.map((file, idx) => (
                        <FileItem
                            key={idx}
                            name={file.name}
                            path={file.path}
                            restoring={restoringIdx === idx}
                            onRestore={() => onRestore(idx)}
                        />
                    ))
                )}
            </div>

            {/* Footer */}
            {files.length > 0 && !loading && (
                <>
                    <div className="rb-divider" />
                    <div className="rb-popup-footer">
                        <button className="rb-btn-empty" onClick={onEmpty}>
                            🗑️ Vaciar Papelera
                        </button>
                    </div>
                </>
            )}
        </div>
    </>
);

/* ── Trash icon widget (bottom-right corner) ── */
const TrashIcon = ({ status, size, numFiles, onClick }) => (
    <div className="recycleBin" onClick={onClick}>
        <img className="img_trash" src="/img/trashBin.png" alt="Trash" />
        <div className="recycleBin-container-items">
            <div className={`recycleText ${status === 'Full' ? 'one' : ''}`}
                 style={{ display: status === 'Full' ? 'flex' : 'none' }}>
                {'Full'.split('').map((ch, i) => (
                    <span key={i} style={{ '--i': i + 1 }}>{ch}</span>
                ))}
            </div>
            <div className={`recycleText ${status === 'Empty' ? 'two' : ''}`}
                 style={{ display: status === 'Empty' ? 'flex' : 'none' }}>
                {'Empty'.split('').map((ch, i) => (
                    <span key={i} style={{ '--i': i + 1 }}>{ch}</span>
                ))}
            </div>
            <ul>
                <li id="txtFile">Size: <b>{size}</b></li>
                <li id="txtSize">Files: <b>{numFiles}</b></li>
            </ul>
        </div>
    </div>
);

/* ── Main exported component ── */
export function RecycleBin() {
    const [isOpen, setIsOpen] = useState(false);
    const [files, setFiles] = useState([]);
    const [binInfo, setBinInfo] = useState({ size: '0 Mb', numFiles: 0, status: 'Empty' });
    const [loading, setLoading] = useState(false);
    const [restoringIdx, setRestoringIdx] = useState(null);

    /* Poll bin info every 1s */
    useEffect(() => {
        const fetchBinInfo = async () => {
            try {
                const res = await axios.get(URL_SERVER.binInfo);
                const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
                const { size, numFiles, status } = data;
                const sizeStr = String(size);
                setBinInfo({
                    size: sizeStr.length > 3
                        ? `${(Number(size) / 1000).toFixed(2)} Gb`
                        : `${size} Mb`,
                    numFiles,
                    status,
                });
            } catch (_) { /* silent */ }
        };

        fetchBinInfo();
        const id = setInterval(fetchBinInfo, 1000);
        return () => clearInterval(id);
    }, []);

    /* Fetch files from recycle bin */
    const fetchFiles = useCallback(async (showLoader = false) => {
        if (showLoader) setLoading(true);
        try {
            const res = await axios.get(URL_SERVER.getInfoFiles);
            const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
            const { names, paths } = data;
            if (names && paths) {
                setFiles(names.map((name, i) => ({ name, path: paths[i] })));
            } else {
                setFiles([]);
            }
        } catch (_) {
            setFiles([]);
        }
        if (showLoader) setLoading(false);
    }, []);

    /* Fetch on open + auto-refresh every 1s while popup is open */
    useEffect(() => {
        if (!isOpen) return;
        fetchFiles(true);
        const id = setInterval(() => fetchFiles(false), 1000);
        return () => clearInterval(id);
    }, [isOpen, fetchFiles]);

    /* Toggle popup */
    const toggle = () => setIsOpen(prev => !prev);
    const close = () => setIsOpen(false);

    /* Restore a single file */
    const handleRestore = async (idx) => {
        const file = files[idx];
        setRestoringIdx(idx);
        try {
            await axios.post(URL_SERVER.restore, { path: file.path });
            await fetchFiles();
        } catch (e) {
            console.error('Restore failed:', e);
        }
        setRestoringIdx(null);
    };

    /* Empty entire bin */
    const handleEmpty = async () => {
        try {
            await axios.get(URL_SERVER.empty);
            setFiles([]);
        } catch (e) {
            console.error('Empty failed:', e);
        }
    };

    return (
        <>
            <TrashIcon
                status={binInfo.status}
                size={binInfo.size}
                numFiles={binInfo.numFiles}
                onClick={toggle}
            />
            <RecycleBinPopup
                isOpen={isOpen}
                files={files}
                onClose={close}
                onRestore={handleRestore}
                onEmpty={handleEmpty}
                loading={loading}
                restoringIdx={restoringIdx}
            />
        </>
    );
}

export default RecycleBin;
