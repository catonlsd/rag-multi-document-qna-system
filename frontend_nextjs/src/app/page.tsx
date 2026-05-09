"use client";

import { useEffect, useRef, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  Upload,
  Send,
  Trash2,
  FileText,
  Activity,
  Database,
  MessageSquare,
  CheckCircle,
  AlertCircle,
  Loader2,
  Copy,
} from "lucide-react";

const BACKEND_URL = "http://127.0.0.1:8000";

type Source = {
  source: string;
  page: number;
  snippet?: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

type Toast = {
  type: "success" | "error" | "info";
  message: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [documents, setDocuments] = useState<string[]>([]);
  const [stats, setStats] = useState({
    total_documents: 0,
    total_chunks: 0,
    total_vectors: 0,
  });

  const [backendOnline, setBackendOnline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [toast, setToast] = useState<Toast | null>(null);

  const chatEndRef = useRef<HTMLDivElement | null>(null);

  const showToast = (type: Toast["type"], message: string) => {
    setToast({ type, message });
    setTimeout(() => setToast(null), 3500);
  };

  const loadDashboard = async () => {
    try {
      await axios.get(`${BACKEND_URL}/health`);
      setBackendOnline(true);

      const docsRes = await axios.get(`${BACKEND_URL}/documents`);
      setDocuments(docsRes.data.documents || []);

      const statsRes = await axios.get(`${BACKEND_URL}/stats`);
      setStats(statsRes.data);
    } catch {
      setBackendOnline(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  const handleUpload = async (file: File | null) => {
    if (!file) return;

    if (file.type !== "application/pdf") {
      showToast("error", "Only PDF files are allowed.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const res = await axios.post(`${BACKEND_URL}/upload`, formData);
      showToast("success", res.data.message || "PDF uploaded successfully.");
      await loadDashboard();
    } catch {
      showToast("error", "Upload failed. Make sure backend is running.");
    } finally {
      setUploading(false);
    }
  };

  const copyAnswer = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      showToast("success", "Answer copied to clipboard.");
    } catch {
      showToast("error", "Failed to copy answer.");
    }
  };

  const handleAsk = async () => {
    if (!query.trim() || loading) return;

    const currentQuery = query;

    const userMessage: Message = {
      role: "user",
      content: currentQuery,
    };

    const updatedMessages = [...messages, userMessage];

    setMessages([
      ...updatedMessages,
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);

    setQuery("");
    setLoading(true);

    try {
      const chatHistory = updatedMessages.slice(-6).map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const streamResponse = await fetch(`${BACKEND_URL}/ask-stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: currentQuery,
          chat_history: chatHistory,
        }),
      });

      if (!streamResponse.body) {
        throw new Error("No response stream.");
      }

      const reader = streamResponse.body.getReader();
      const decoder = new TextDecoder();

      let finalAnswer = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);
        finalAnswer += chunk;

        setMessages((prev) => {
          const updated = [...prev];

          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: finalAnswer,
          };

          return updated;
        });
      }

      const sourceRes = await axios.post(`${BACKEND_URL}/ask`, {
        query: currentQuery,
        chat_history: chatHistory,
      });

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: finalAnswer || sourceRes.data.answer || "No answer found.",
          sources: sourceRes.data.sources || [],
        };

        return updated;
      });

      await loadDashboard();
    } catch {
      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: "Backend error. Please check FastAPI server.",
        };

        return updated;
      });

      showToast("error", "Failed to generate answer.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      setLoading(true);
      await axios.delete(`${BACKEND_URL}/reset`);
      setMessages([]);
      showToast("success", "Knowledge base reset successfully.");
      await loadDashboard();
    } catch {
      showToast("error", "Reset failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      {toast && (
        <div className="fixed right-6 top-6 z-50">
          <div
            className={`flex items-center gap-3 rounded-2xl border px-5 py-4 shadow-2xl ${
              toast.type === "success"
                ? "border-emerald-700 bg-emerald-950 text-emerald-200"
                : toast.type === "error"
                ? "border-red-700 bg-red-950 text-red-200"
                : "border-slate-700 bg-slate-900 text-slate-200"
            }`}
          >
            {toast.type === "success" ? (
              <CheckCircle size={20} />
            ) : (
              <AlertCircle size={20} />
            )}
            <span className="text-sm font-medium">{toast.message}</span>
          </div>
        </div>
      )}

      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[320px_1fr]">
        <aside className="border-r border-slate-800 bg-slate-900/70 p-6">
          <div className="mb-8">
            <h2 className="flex items-center gap-2 text-xl font-bold">
              <Database size={22} />
              RAG Dashboard
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              Manage documents and knowledge base.
            </p>
          </div>

          <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="mb-3 flex items-center gap-2 font-semibold">
              <Activity size={18} />
              System Status
            </h3>

            <div
              className={`rounded-xl px-3 py-2 text-sm ${
                backendOnline
                  ? "bg-emerald-500/15 text-emerald-300"
                  : "bg-red-500/15 text-red-300"
              }`}
            >
              {backendOnline ? "Backend connected" : "Backend offline"}
            </div>
          </section>

          <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="mb-4 font-semibold">Knowledge Base Stats</h3>

            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="rounded-xl bg-slate-900 p-3">
                <p className="text-2xl font-bold">{stats.total_documents}</p>
                <p className="text-xs text-slate-400">Docs</p>
              </div>

              <div className="rounded-xl bg-slate-900 p-3">
                <p className="text-2xl font-bold">{stats.total_chunks}</p>
                <p className="text-xs text-slate-400">Chunks</p>
              </div>

              <div className="rounded-xl bg-slate-900 p-3">
                <p className="text-2xl font-bold">{stats.total_vectors}</p>
                <p className="text-xs text-slate-400">Vectors</p>
              </div>
            </div>
          </section>

          <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="mb-3 flex items-center gap-2 font-semibold">
              <Upload size={18} />
              Upload PDF
            </h3>

            <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-900 p-6 text-center hover:border-indigo-400">
              {uploading ? (
                <Loader2 className="mb-2 animate-spin text-indigo-300" />
              ) : (
                <Upload className="mb-2 text-slate-400" />
              )}

              <span className="text-sm text-slate-300">
                {uploading ? "Processing PDF..." : "Choose PDF"}
              </span>

              <input
                type="file"
                accept="application/pdf"
                className="hidden"
                disabled={uploading}
                onChange={(e) => handleUpload(e.target.files?.[0] || null)}
              />
            </label>
          </section>

          <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="mb-3 flex items-center gap-2 font-semibold">
              <FileText size={18} />
              Processed Documents
            </h3>

            <div className="max-h-56 space-y-2 overflow-y-auto pr-1">
              {documents.length === 0 ? (
                <p className="text-sm text-slate-400">No documents uploaded.</p>
              ) : (
                documents.map((doc) => (
                  <div
                    key={doc}
                    className="rounded-xl bg-slate-900 px-3 py-2 text-sm text-slate-300"
                  >
                    {doc}
                  </div>
                ))
              )}
            </div>
          </section>

          <button
            onClick={() => setMessages([])}
            className="mb-3 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 text-sm hover:bg-slate-800"
          >
            <MessageSquare size={16} />
            Clear Chat
          </button>

          <button
            onClick={handleReset}
            disabled={loading || uploading}
            className="flex w-full items-center justify-center gap-2 rounded-xl border border-red-800/70 px-4 py-3 text-sm text-red-300 hover:bg-red-950/40 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Trash2 size={16} />
            Reset Knowledge Base
          </button>
        </aside>

        <section className="flex min-h-screen flex-col">
          <header className="border-b border-slate-800 px-8 py-6">
            <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
              📚 Multi-Document RAG QnA System
            </h1>

            <p className="mt-2 text-slate-400">
              Ask questions across multiple PDFs using hybrid search, reranking,
              and conversational memory.
            </p>
          </header>

          <div className="flex-1 space-y-6 overflow-y-auto px-8 py-8">
            {messages.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <div className="max-w-xl text-center">
                  <h2 className="text-2xl font-semibold">
                    Start asking questions
                  </h2>

                  <p className="mt-3 text-slate-400">
                    Upload PDFs from the sidebar, then ask anything from your
                    documents.
                  </p>
                </div>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`rounded-2xl border p-5 ${
                    msg.role === "user"
                      ? "border-indigo-800 bg-indigo-950/30"
                      : "border-slate-800 bg-slate-900"
                  }`}
                >
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      {msg.role}
                    </p>

                    {msg.role === "assistant" && msg.content && (
                      <button
                        onClick={() => copyAnswer(msg.content)}
                        className="flex items-center gap-1 rounded-lg border border-slate-700 px-2 py-1 text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                      >
                        <Copy size={13} />
                        Copy
                      </button>
                    )}
                  </div>

                  {msg.role === "assistant" && loading && !msg.content ? (
                    <div className="flex items-center gap-3 text-slate-300">
                      <Loader2 className="animate-spin" size={20} />
                      Searching documents and generating answer...
                    </div>
                  ) : (
                    <div className="max-w-none space-y-4 text-slate-200">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({ children }) => (
                            <h1 className="mb-4 text-3xl font-bold">
                              {children}
                            </h1>
                          ),
                          h2: ({ children }) => (
                            <h2 className="mb-3 text-2xl font-semibold">
                              {children}
                            </h2>
                          ),
                          h3: ({ children }) => (
                            <h3 className="mb-2 text-xl font-semibold">
                              {children}
                            </h3>
                          ),
                          p: ({ children }) => (
                            <p className="leading-7 text-slate-300">
                              {children}
                            </p>
                          ),
                          ul: ({ children }) => (
                            <ul className="list-disc space-y-2 pl-6">
                              {children}
                            </ul>
                          ),
                          ol: ({ children }) => (
                            <ol className="list-decimal space-y-2 pl-6">
                              {children}
                            </ol>
                          ),
                          li: ({ children }) => <li>{children}</li>,
                          code: ({ children }) => (
                            <code className="rounded bg-slate-800 px-2 py-1 text-indigo-300">
                              {children}
                            </code>
                          ),
                          pre: ({ children }) => (
                            <pre className="overflow-x-auto rounded-2xl bg-black p-4 text-sm">
                              {children}
                            </pre>
                          ),
                          strong: ({ children }) => (
                            <strong className="font-semibold text-white">
                              {children}
                            </strong>
                          ),
                          table: ({ children }) => (
                            <div className="overflow-x-auto">
                              <table className="w-full border-collapse border border-slate-700">
                                {children}
                              </table>
                            </div>
                          ),
                          thead: ({ children }) => (
                            <thead className="bg-slate-800">{children}</thead>
                          ),
                          tbody: ({ children }) => <tbody>{children}</tbody>,
                          tr: ({ children }) => (
                            <tr className="border-b border-slate-700">
                              {children}
                            </tr>
                          ),
                          th: ({ children }) => (
                            <th className="border border-slate-700 px-4 py-3 text-left font-semibold text-white">
                              {children}
                            </th>
                          ),
                          td: ({ children }) => (
                            <td className="border border-slate-700 px-4 py-3 text-slate-300">
                              {children}
                            </td>
                          ),
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  )}

                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-5">
                      <p className="mb-3 text-sm font-semibold text-slate-300">
                        Sources
                      </p>

                      <div className="grid gap-3 md:grid-cols-2">
                        {msg.sources.map((source, i) => (
                          <div
                            key={i}
                            className="rounded-2xl border border-slate-700 bg-slate-950 p-4"
                          >
                            <div className="mb-2 flex items-center justify-between gap-3">
                              <p className="font-medium text-slate-200">
                                {source.source}
                              </p>

                              <span className="rounded-full bg-indigo-500/15 px-3 py-1 text-xs text-indigo-300">
                                Page {source.page}
                              </span>
                            </div>

                            {source.snippet && (
                              <p className="line-clamp-3 text-sm leading-6 text-slate-400">
                                {source.snippet}...
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}

            <div ref={chatEndRef} />
          </div>

          <div className="border-t border-slate-800 bg-slate-950 p-6">
            <div className="mx-auto flex max-w-5xl gap-3">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleAsk();
                }}
                disabled={loading}
                placeholder="Ask something from your uploaded documents..."
                className="flex-1 rounded-2xl border border-slate-700 bg-slate-900 px-5 py-4 outline-none focus:border-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
              />

              <button
                onClick={handleAsk}
                disabled={loading || !query.trim()}
                className="flex items-center justify-center rounded-2xl bg-indigo-600 px-6 py-4 font-semibold hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? (
                  <Loader2 className="animate-spin" size={20} />
                ) : (
                  <Send size={20} />
                )}
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}