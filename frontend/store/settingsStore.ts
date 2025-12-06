import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// 支持的模型列表
export const AVAILABLE_MODELS = [
  { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', description: '快速响应，适合一般使用' },
  { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', description: '更强能力，适合复杂内容' },
] as const;

export type ModelId = typeof AVAILABLE_MODELS[number]['id'];

interface SettingsState {
  // API 配置
  apiKey: string;
  model: ModelId;

  // 是否已配置
  isConfigured: boolean;

  // Actions
  setApiKey: (key: string) => void;
  setModel: (model: ModelId) => void;
  clearSettings: () => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      apiKey: '',
      model: 'gemini-2.5-flash',
      isConfigured: false,

      setApiKey: (key) => set({
        apiKey: key,
        isConfigured: key.trim().length > 0
      }),

      setModel: (model) => set({ model }),

      clearSettings: () => set({
        apiKey: '',
        model: 'gemini-2.5-flash',
        isConfigured: false
      }),
    }),
    {
      name: 'unitutor-settings',
      // 只持久化这些字段
      partialize: (state) => ({
        apiKey: state.apiKey,
        model: state.model,
        isConfigured: state.isConfigured,
      }),
    }
  )
);
