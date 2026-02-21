import { Fragment, useEffect, useRef, useState } from 'react';
import './styles/main.css';
import VanilaTilt from 'vanilla-tilt';
import axios from 'axios';
import { RecycleBin } from './components/RecycleBin.jsx';

// Componente principal de la página
function MainPage() {
    const tileRef = useRef();
    const [isScheduleVisible, setIsScheduleVisible] = useState(true);
    const [config, setConfig] = useState({ blur: true, trash: true, activeWeek: 'A' });

    useEffect(() => {
        VanilaTilt.init(tileRef.current, {
            max: 10,
            speed: 800,
            glare: true,
            "max-glare": 0.3,
            perspective: 1400
        });

        return () => {
            tileRef.current.vanillaTilt.destroy();
        };
    }, []);

    /* Poll config every 1s */
    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const res = await axios.get('http://localhost:5000/api/config');
                setConfig(res.data);
            } catch (_) {}
        };
        fetchConfig();
        const id = setInterval(fetchConfig, 1000);
        return () => clearInterval(id);
    }, []);

    const toggleScheduleVisibility = () => {
        setIsScheduleVisible(prevState => !prevState);
    };

    return (
        <Fragment>
            <div className="fondo" style={{ filter: config.blur ? 'blur(5px)' : 'none' }}>
                <img src="/img/wallpaper.jpg" alt="Fondo" />
            </div>
            {config.trash && <RecycleBin />}
            <div
                id="horario"
                ref={tileRef}
                style={{ display: isScheduleVisible ? 'flex' : 'none' }}
            >
                <Table activeWeek={config.activeWeek} />
            </div>
            <button onClick={toggleScheduleVisibility} className='btnHide'>
                {isScheduleVisible ? 'Hide' : 'Show'}
            </button>
        </Fragment>
    );
}

// Componente de la tabla
function Table({ activeWeek }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://localhost:5000/api/data");
                setData(response.data);
            } catch (error) {
                console.error("Error fetching data:", error.message);
            }
        };
        fetchData();
    }, [activeWeek]);

    if (!data) {
        return null;
    }

    return (
        <table>
            <Thead headTable={data.head_table} />
            <Tbody rowsValues={data.rows_values} />
        </table>
    );
}

// Componente para el encabezado de la tabla
function Thead({ headTable }) {
    if (!headTable) {
        return null;
    }

    return (
        <thead>
            <tr>
                {headTable.map((item, index) => (
                    <th key={index}>{item}</th>
                ))}
            </tr>
        </thead>
    );
}

// Componente para el cuerpo de la tabla
function Tbody({ rowsValues }) {
    if (!rowsValues) {
        return null;
    }

    return (
        <tbody>
            {rowsValues.map((item, rowIndex) => (
                <tr key={rowIndex}>
                    {item.map((subItem, cellIndex) => (
                        <td key={cellIndex}>{subItem}</td>
                    ))}
                </tr>
            ))}
        </tbody>
    );
}

// Componente principal de la aplicación
export function App() {
    return <MainPage />;
}
