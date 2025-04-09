import React, { useState } from "react";
import axios from "axios";
import ChatMessage from "./components/ChatMessage";
import { Message } from "./types/Message";
import { v4 as uuidv4 } from "uuid";
import "./App.css";

let sessionId = localStorage.getItem("session_id");

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [image, setImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<string>("auto"); // New state for agent selection

  const handleSend = async () => {
    if (!text && !image) return;
    setLoading(true);

    const userMessage: Message = {
      id: uuidv4(),
      role: "user",
      content: text,
      image: image ?? undefined,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const payload = {
        text: text,
        image: image || null,
        session_id: sessionId || null, // Include session ID if available
        agent: selectedAgent === "auto" ? null : selectedAgent, // Include agent if selected
      };

      const res = await axios.post("http://localhost:8000/chat", payload);

      // Store session ID if it's a new session
      if (!sessionId && res.data.session_id) {
        sessionId = res.data.session_id;
        localStorage.setItem("session_id", sessionId || "");
      }

      const data = res.data;

      const botMessage: Message = {
        id: uuidv4(),
        role: "bot",
        content: data.response || data.error || "Something went wrong.",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const botMessage: Message = {
        id: uuidv4(),
        role: "bot",
        content: "Failed to send message. Please try again.",
      };

      setMessages((prev) => [...prev, botMessage]);
    } finally {
      setText("");
      setImage(null);
      setLoading(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = (reader.result as string).split(",")[1];
      setImage(base64);
    };

    reader.readAsDataURL(file);
  };

  const handleNewSession = () => {
    sessionId = null;
    localStorage.removeItem("session_id");
    setMessages([]);
  };

  return (
    <div className="App">
      <h1>Property Loop</h1>

      <div className="chat-window">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {loading && <div className="chat-bubble bot">🤖 Typing...</div>}
      </div>

      <div className="input-area">
        <select
          value={selectedAgent}
          onChange={(e) => setSelectedAgent(e.target.value)}
        >
          <option value="auto">Auto</option>
          <option value="faq">FAQ Agent</option>
          <option value="vision">Vision Agent</option>
        </select>
        <input
          type="text"
          placeholder="Ask something..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        {["auto", "vision"].includes(selectedAgent) && (
          <input type="file" accept="image/*" onChange={handleFileUpload} />
        )}
        <button onClick={handleSend}>Send</button>
        <button onClick={handleNewSession}>New Session</button>
      </div>
    </div>
  );
}

export default App;
