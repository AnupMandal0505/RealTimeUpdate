import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:8000/api';

function AppointmentTest() {
    const [appointments, setAppointments] = useState([]);

    // WebSocket setup
    useEffect(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/database_updates/`;
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            console.log('WebSocket Connected');
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log('WebSocket message received:', message);
            
            if (message.type === 'initial_data' || message.type === 'update') {
                setAppointments(message.data);
            }
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        socket.onclose = () => {
            console.log('WebSocket Disconnected');
        };

        return () => {
            socket.close();
        };
    }, []);

    // Initial data fetch
    useEffect(() => {
        fetch(`${API_BASE_URL}/appointments/`)
            .then(response => response.json())
            .then(data => setAppointments(data.data))
            .catch(error => console.error('Error fetching appointments:', error));
    }, []);

    return (
        <div>
            <h2>Appointments</h2>
            <div>
                {appointments.map(appointment => (
                    <div key={appointment.id} style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
                        <p>Name: {appointment.name}</p>
                        <p>Status: {appointment.status}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default AppointmentTest; 