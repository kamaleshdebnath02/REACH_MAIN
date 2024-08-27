import React, { useState, useEffect, useCallback } from 'react';
import './Chatbot.css';
import axios from 'axios';

function Chatbot() {
    const generateUserId = () => {
        const newUserId = Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userId', newUserId);
        return newUserId;
    };

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [userId] = useState(localStorage.getItem('userId') || generateUserId());
    const [speech] = useState(() => {
        const speechSynth = new SpeechSynthesisUtterance();
        speechSynth.voice = speechSynthesis.getVoices().find(voice => voice.lang === 'en-US');
        return speechSynth;
    });

    const speak = useCallback((text) => {
        speech.text = text;
        window.speechSynthesis.speak(speech);
    }, [speech]);

    useEffect(() => {
        const sendInitialGreeting = () => {
            const greeting = "Hello! I'm here to help you with your health queries.";
            const timestamp = new Date().toLocaleTimeString();
            setMessages([{ text: greeting, fromUser: false, timestamp }]);
        };
        sendInitialGreeting();
    }, []);

    const handleSendClick = async () => {
        if (!input.trim()) return;
        setIsLoading(true);
        const userMessage = { text: input, fromUser: true, timestamp: new Date().toLocaleTimeString() };
        setMessages(prevMessages => [...prevMessages, userMessage]);

        try {
            const response = await axios.post('/chat', { message: input, user_id: userId });
            const { response: botResponse, image } = response.data;

            const botMessage = { text: botResponse, fromUser: false, timestamp: new Date().toLocaleTimeString(), image };

            setTimeout(() => {
                setMessages(prevMessages => [...prevMessages, botMessage]);
            }, 2000);

        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = 'Error: Could not send message.';
            const botMessage = { text: errorMessage, fromUser: false, timestamp: new Date().toLocaleTimeString() };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } finally {
            setIsLoading(false);
        }
        setInput('');
    };

    const translateMessage = async (text, lang) => {
        try {
            const response = await axios.post('/translate', { text, lang });
            return response.data.translated_text;
        } catch (error) {
            console.error('Error translating message:', error);
            return 'Error: Could not translate message.';
        }
    };

    const handleTranslateClick = async (text) => {
        const translatedText = await translateMessage(text, 'bn');  // Translate to Bengali
        if (!translatedText.startsWith('Error:')) {
            const translatedMessage = { text: translatedText, fromUser: false, timestamp: new Date().toLocaleTimeString() };
            setMessages(prevMessages => [...prevMessages, translatedMessage]);
        } else {
            const errorMessage = { text: translatedText, fromUser: false, timestamp: new Date().toLocaleTimeString() };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        }
    };

    const handleSpeakClick = (text) => {
        speak(text);
    };

    return (
        <div className="chatbot-container">
            <div className="chat-window">
                <div className="messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.fromUser ? 'user' : 'bot'}`}>
                            <div className="message-text">
                                {msg.text}
                                {msg.image && <img src={msg.image} alt="bot response" className="response-image" />}
                                {!msg.fromUser && (
                                    <>
                                        <button onClick={() => handleTranslateClick(msg.text)}>Translate</button>
                                        <button onClick={() => handleSpeakClick(msg.text)} className="mic-button">🎤</button>
                                    </>
                                )}
                            </div>
                            <div className="timestamp">{msg.timestamp}</div>
                        </div>
                    ))}
                    {isLoading && <div className="message bot">Bot is typing...</div>}
                </div>
                <div className="input-area">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={e => e.key === 'Enter' && handleSendClick()}
                        placeholder="Type your message here..."
                    />
                    <button onClick={handleSendClick}>Send</button>
                </div>
            </div>
        </div>
    );
}

export default Chatbot;
