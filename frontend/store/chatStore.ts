import { create } from 'zustand';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
}

interface ChatState {
  // 聊天状态
  messages: ChatMessage[];
  isOpen: boolean;
  isLoading: boolean;
  currentPageContext: number; // 当前上下文对应的页码

  // Actions
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => string;
  updateMessage: (id: string, content: string, isStreaming?: boolean) => void;
  setIsOpen: (isOpen: boolean) => void;
  setIsLoading: (isLoading: boolean) => void;
  clearMessages: () => void;
  setCurrentPageContext: (page: number) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  // 初始状态
  messages: [],
  isOpen: false,
  isLoading: false,
  currentPageContext: 1,

  // Actions
  addMessage: (message) => {
    const id = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newMessage: ChatMessage = {
      ...message,
      id,
      timestamp: new Date(),
    };
    set((state) => ({
      messages: [...state.messages, newMessage],
    }));
    return id;
  },

  updateMessage: (id, content, isStreaming = false) => {
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, content, isStreaming } : msg
      ),
    }));
  },

  setIsOpen: (isOpen) => set({ isOpen }),

  setIsLoading: (isLoading) => set({ isLoading }),

  clearMessages: () => set({ messages: [] }),

  setCurrentPageContext: (page) => {
    const state = get();
    // 如果页面变化，清空聊天记录
    if (state.currentPageContext !== page) {
      set({ currentPageContext: page, messages: [] });
    }
  },
}));
