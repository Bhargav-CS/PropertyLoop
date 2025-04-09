export interface Message {
    id: string;
    role: 'user' | 'bot';
    content: string;
    image?: string; // base64 image string (optional)
  }
  