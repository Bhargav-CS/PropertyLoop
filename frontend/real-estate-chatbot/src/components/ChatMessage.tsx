import React from "react";
import { Message } from "../types/Message";
import "./ChatMessage.css"; // Optional for scoped styles

interface Props {
  message: Message;
}

const ChatMessage: React.FC<Props> = ({ message }) => {
  return (
    <div
      className={`chat-bubble ${message.role === "user" ? "user" : "bot"}`}
    >
      {message.image && (
        <img
          src={`data:image/jpeg;base64,${message.image}`}
          alt="User upload"
          className="chat-image"
        />
      )}
      <p>{message.content}</p>
    </div>
  );
};

export default ChatMessage;
