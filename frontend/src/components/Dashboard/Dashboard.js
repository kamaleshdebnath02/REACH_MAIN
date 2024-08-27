import React, { useState } from 'react';
import './Dashboard.css';
import * as XLSX from 'xlsx';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { Container, Row, Col, Card, Table, ProgressBar, Button } from 'react-bootstrap';

// Register the components required for the chart
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

function Dashboard() {
    const [data, setData] = useState([]);
    const [chartData, setChartData] = useState({});
    const [fileName, setFileName] = useState('');
    const [insights, setInsights] = useState({ avg: 0, max: 0, min: 0 });
    const [comments, setComments] = useState([]);

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        setFileName(file.name);

        const reader = new FileReader();
        reader.onload = (event) => {
            const binaryStr = event.target.result;
            const workbook = XLSX.read(binaryStr, { type: 'binary' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet);
            setData(jsonData);
            generateChartData(jsonData);
            calculateInsightsAndComments(jsonData);
        };
        reader.readAsBinaryString(file);
    };

    const generateChartData = (data) => {
        const dateColumns = Object.keys(data[0]).slice(3, -1); // Columns starting from the fourth column (dates) up to the second last column (excluding phone)
        const attendanceCounts = dateColumns.map(date => 
            data.reduce((acc, curr) => acc + parseInt(curr[date]), 0)
        );

        setChartData({
            labels: dateColumns,
            datasets: [
                {
                    label: 'Overall Attendance',
                    data: attendanceCounts,
                    backgroundColor: 'rgba(75,192,192,0.6)',
                    borderColor: 'rgba(75,192,192,1)',
                    borderWidth: 1,
                },
            ],
        });
    };

    const calculateInsightsAndComments = (data) => {
        const totalDays = Object.keys(data[0]).length - 4; // Total days is total columns minus Roll No, Name, Phone, and 1 extra
        const newComments = data.map(student => {
            const attendanceArray = Object.values(student).slice(3, -1).map(Number); // Skip first three columns (Roll No, Name, Phone) and last column
            const attendanceCount = attendanceArray.reduce((sum, present) => sum + present, 0);
            const attendancePercentage = (attendanceCount / totalDays) * 100;

            let comment = '';
            if (attendancePercentage === 100) {
                comment = `Your Child ${student['Name']} has Excellent attendance!`;
            } else if (attendancePercentage >= 75) {
                comment = `Your Child ${student['Name']} has Good attendance, keep it up!`;
            } else if (attendancePercentage >= 50) {
                comment = `Your Child ${student['Name']} needs improvement, needs to attend more classes.`;
            } else {
                comment = `Your Child ${student['Name']} has Poor attendance, at risk of failing.`;
            }

            return {
                name: student['Name'],
                rollNo: student['Roll No.'],
                phone: student['phone'],  // Phone number for sending messages
                percentage: attendancePercentage.toFixed(2),
                comment,
            };
        });

        const averageAttendance = newComments.reduce((sum, student) => sum + parseFloat(student.percentage), 0) / newComments.length;
        const maxAttendance = Math.max(...newComments.map(student => parseFloat(student.percentage)));
        const minAttendance = Math.min(...newComments.map(student => parseFloat(student.percentage)));

        setComments(newComments);
        setInsights({ avg: averageAttendance.toFixed(2), max: maxAttendance, min: minAttendance });
    };

    const handleSendMessage = async (phone, message) => {
        try {
            if (!phone || !message) {
                throw new Error('Phone number or message is missing');
            }
    
            // Ensure phone is a string and starts with a '+'
            phone = String(phone); // Convert to string if it's not already
            if (!phone.startsWith('+')) {
                phone = `+${phone}`;
            }
    
            console.log('Sending message to:', phone);
            console.log('Message:', message);
    
            // Send the data as JSON to the backend
            const response = await fetch('http://localhost:5000/send-whatsapp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ phone, message }),  // Sending the data as JSON
            });
    
            if (response.ok) {
                alert(`Message sending initiated to ${phone}`);
            } else {
                const errorText = await response.text();
                alert(`Failed to send message: ${errorText}`);
            }
        } catch (error) {
            alert(`Error sending message: ${error.message}`);
        }
    };

    return (
        <Container fluid className="dashboard-container">
            <Row className="mb-4">
                <Col>
                    <Card className="upload-card">
                        <h2 className="dashboard-title">Analytics Dashboard</h2>
                        <p className="dashboard-description">Upload your CSV file to visualize attendance data.</p>
                        <input
                            type="file"
                            accept=".csv, .xlsx, .xls"
                            onChange={handleFileUpload}
                            className="file-upload-btn"
                        />
                        {fileName && <p className="file-name">Uploaded: {fileName}</p>}
                    </Card>
                </Col>
            </Row>

            <Row>
                <Col md={8}>
                    <Card className="chart-card">
                        <h4>Attendance Overview</h4>
                        {data.length > 0 ? (
                            <div className="chart-container">
                                <Bar data={chartData} />
                            </div>
                        ) : (
                            <p>No data available. Please upload a CSV file.</p>
                        )}
                    </Card>
                </Col>
                <Col md={4}>
                    <Card className="insights-card">
                        <h4>Data Insights</h4>
                        <p>Average Attendance: {insights.avg}%</p>
                        <p>Max Attendance: {insights.max}%</p>
                        <p>Min Attendance: {insights.min}%</p>
                        <ProgressBar now={insights.avg} label={`${insights.avg}%`} />
                    </Card>
                </Col>
            </Row>

            <Row className="mt-4">
                <Col>
                    <Card className="table-card">
                        <h4>Student Comments and Data</h4>
                        {comments.length > 0 ? (
                            <Table responsive className="data-table">
                                <thead>
                                    <tr>
                                        <th>Roll No</th>
                                        <th>Name</th>
                                        <th>Phone</th>
                                        <th>Attendance Percentage</th>
                                        <th>Comments</th>
                                        <th>Send WhatsApp</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {comments.map((student, index) => (
                                        <tr key={index}>
                                            <td>{student.rollNo}</td>
                                            <td>{student.name}</td>
                                            <td>{student.phone}</td>
                                            <td>{student.percentage}%</td>
                                            <td>{student.comment}</td>
                                            <td>
                                                <Button 
                                                    variant="primary" 
                                                    onClick={() => handleSendMessage(student.phone, student.comment)}
                                                >
                                                    Send
                                                </Button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                        ) : (
                            <p>No data available. Please upload a CSV file.</p>
                        )}
                    </Card>
                </Col>
            </Row>
        </Container>
    );
}

export default Dashboard;
