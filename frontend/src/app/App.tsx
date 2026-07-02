import { useState, useRef, useEffect } from "react";
import { Search, ArrowUp, RotateCcw, Sparkles, Copy, ThumbsUp, ThumbsDown, Share2 } from "lucide-react";

const MOCK_ANSWERS: Record<string, { answer: string; sources: { title: string; domain: string }[] }> = {
  default: {
    answer: `Retrieval-Augmented Generation (RAG) is an AI architecture that enhances large language model outputs by grounding them in external, up-to-date knowledge sources.\n\nInstead of relying solely on information baked into model weights during training, RAG systems retrieve relevant documents from a knowledge base at inference time, then synthesize a response using both the retrieved context and the model's reasoning capabilities.\n\nThis approach offers two core advantages: it reduces hallucination by anchoring responses in verifiable source material, and it allows models to stay current without expensive retraining cycles. The retrieval step typically uses a combination of sparse (BM25) and dense (vector similarity) search, often followed by a cross-encoder reranking pass to select the most relevant passages before generation.`,
    sources: [
      { title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", domain: "arxiv.org" },
      { title: "Dense Passage Retrieval for Open-Domain QA", domain: "aclanthology.org" },
      { title: "REALM: Retrieval-Augmented Language Model Pre-Training", domain: "proceedings.mlr.press" },
    ],
  },
};

// Extracts and groups the context output by Tool Name
const parseContextByTool = (contextString) => {
  if (!contextString) return [];
  
  // Split the string by "ToolName(name="
  const sections = contextString.split("ToolName(name=");
  const parsed = [];

  sections.forEach((sec) => {
    if (!sec.trim()) return;
    
    // Extract the tool name and the remaining payload
    // Matches "'TOOL_NAME'): {payload}"
    const match = sec.match(/^'([^']+)'\):\s*([\s\S]*)/);
    if (match) {
      parsed.push({
        tool: match[1],
        output: match[2].trim()
      });
    }
  });
  
  return parsed;
};

// Keep your existing parseExecutionPlan function too!
const parseExecutionPlan = (planString) => {
  if (!planString) return [];
  const lines = planString.split('\n').filter(line => line.includes('->'));
  return lines.map(line => {
    return line.split('->').map(step => {
      const match = step.match(/name='([^']+)'/);
      return match ? match[1] : step.trim();
    });
  });
};


// Extracts the actual documents from the messy context string
const extractDocuments = (contextString) => {
  if (!contextString) return [];
  
  const documents = [];
  // Regex to hunt down the id, title, and content inside the Python dictionary string
  const docRegex = /'id':\s*'([^']+)',\s*'title':\s*'([^']+)',\s*'content':\s*'([^']+)'/g;
  
  let match;
  while ((match = docRegex.exec(contextString)) !== null) {
    documents.push({
      id: match[1],
      title: match[2],
      content: match[3]
    });
  }
  return documents;
};

const EXAMPLE_QUERIES = [
  "Google phones give me",
  "New Good phones to buy",
  "Phones under 700",
  "phones with good battery life",
];

type Phase = "idle" | "thinking" | "streaming" | "done";

function useTypewriter(text: string, active: boolean) {
  const [displayed, setDisplayed] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!active) { setDisplayed(""); setDone(false); return; }
    setDisplayed("");
    setDone(false);
    let i = 0;
    const interval = setInterval(() => {
      i += Math.floor(Math.random() * 4) + 2;
      if (i >= text.length) {
        setDisplayed(text);
        setDone(true);
        clearInterval(interval);
      } else {
        setDisplayed(text.slice(0, i));
      }
    }, 18);
    return () => clearInterval(interval);
  }, [text, active]);

  return { displayed, done };
}

function ThinkingDots() {
  return (
    <div className="flex items-center gap-1.5">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full"
          style={{
            background: "#1b4dff",
            animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
          }}
        />
      ))}
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
          40% { transform: translateY(-5px); opacity: 1; }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(6px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
        .fade-in { animation: fadeIn 0.4s ease forwards; }
        .cursor-blink::after {
          content: '▋';
          color: #1b4dff;
          animation: blink 0.9s step-end infinite;
          margin-left: 1px;
        }
        @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
      `}</style>
    </div>
  );
}

export default function App() {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState("");
  const [phase, setPhase] = useState<Phase>("idle"); // Assuming Phase is "idle" | "thinking" | "streaming" | "error"
  const [copied, setCopied] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // NEW: State to hold the real API response
  const [answerData, setAnswerData] = useState<any | null>(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleSubmit = async (q = query) => {
    if (!q.trim() || phase === "thinking" || phase === "streaming") return;
    
    setSubmittedQuery(q.trim());
    setPhase("thinking");
    setErrorMsg(null);

    try {
      // REPLACE "/your-endpoint" with your actual FastAPI route!
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST", // Assuming POST since you are sending a query
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: q.trim() }), 
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Check if your API returned success based on your terminal output
      if (data.success) {
        setAnswerData(data); // Save the whole payload (answer, metadata, plan)
        setPhase("streaming");
      } else {
        throw new Error(data.error || "API returned an unsuccessful response");
      }

    } catch (error) {
      console.error("Failed to fetch from API:", error);
      setErrorMsg(error.message);
      setPhase("idle"); // Reset phase or set to an "error" phase if you have one
    }
  };

  // Safely extract the answer string for the typewriter
  const textToStream = answerData?.answer?.answer || "";
  const { displayed, done } = useTypewriter(textToStream, phase === "streaming");

  useEffect(() => {
    if (done && phase === "streaming") {
      setPhase("done");
    }
  }, [done, phase]);

  const handleReset = () => {
    setPhase("idle");
    setQuery("");
    setSubmittedQuery("");
    setTimeout(() => inputRef.current?.focus(), 50);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(answerData.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  const isActive = phase !== "idle";

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{
        background: "#0a0a0f",
        fontFamily: "Inter, sans-serif",
      }}
    >
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <div
            className="w-7 h-7 rounded-lg flex items-center justify-center"
            style={{ background: "linear-gradient(135deg, #1b4dff, #7c3aed)" }}
          >
            <Sparkles size={13} className="text-white" />
          </div>
          <span style={{ color: "#e2e8f0", fontSize: "14px", fontWeight: 600, letterSpacing: "-0.02em" }}>
            Arcana
          </span>
        </div>
        <div className="flex items-center gap-2">
          {isActive && (
            <button
              onClick={handleReset}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors fade-in"
              style={{
                color: "#6b7280",
                fontSize: "12px",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.06)",
              }}
            >
              <RotateCcw size={11} />
              New search
            </button>
          )}
        </div>
      </header>

      {/* Main content */}
      <main
        className="flex-1 flex flex-col items-center px-4"
        style={{
          paddingTop: isActive ? "40px" : "22vh",
          transition: "padding-top 0.5s cubic-bezier(0.16, 1, 0.3, 1)",
          maxWidth: "100%",
        }}
      >
        {/* Logo / title — only when idle */}
        {!isActive && (
          <div className="text-center mb-8 fade-in">
            <div
              className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4"
              style={{ background: "linear-gradient(135deg, rgba(27,77,255,0.2), rgba(124,58,237,0.2))", border: "1px solid rgba(27,77,255,0.2)" }}
            >
              <Sparkles size={24} style={{ color: "#7c8cff" }} />
            </div>
            <h1
              style={{
                color: "#e2e8f0",
                fontSize: "28px",
                fontWeight: 600,
                letterSpacing: "-0.03em",
                lineHeight: 1.2,
              }}
            >
              Ask anything
            </h1>
            <p style={{ color: "#4b5563", fontSize: "14px", marginTop: "6px" }}>
              Get instant, sourced answers from your document corpus
            </p>
          </div>
        )}

        {/* Search bar */}
        <div
          className="w-full"
          style={{ maxWidth: "680px" }}
        >
          <div
            className="relative flex items-center rounded-2xl transition-all"
            style={{
              background: "#111118",
              border: `1px solid ${phase === "thinking" || phase === "streaming" ? "rgba(27,77,255,0.4)" : "rgba(255,255,255,0.08)"}`,
              boxShadow: phase !== "idle"
                ? "0 0 0 3px rgba(27,77,255,0.08), 0 20px 60px rgba(0,0,0,0.4)"
                : "0 8px 32px rgba(0,0,0,0.3)",
              transition: "all 0.3s ease",
            }}
          >
            <Search
              size={16}
              className="ml-4 shrink-0"
              style={{ color: phase === "thinking" ? "#1b4dff" : "#4b5563", transition: "color 0.3s" }}
            />
            <input
              ref={inputRef}
              value={isActive ? submittedQuery : query}
              onChange={(e) => !isActive && setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="Ask anything…"
              readOnly={isActive}
              autoFocus
              style={{
                flex: 1,
                background: "transparent",
                border: "none",
                outline: "none",
                color: "#e2e8f0",
                fontSize: "15px",
                padding: "14px 12px",
                fontFamily: "Inter, sans-serif",
                cursor: isActive ? "default" : "text",
              }}
            />
            {phase === "thinking" || phase === "streaming" ? (
              <div className="mr-4">
                <ThinkingDots />
              </div>
            ) : (
              <button
                onClick={() => handleSubmit()}
                disabled={!query.trim()}
                className="mr-2 w-8 h-8 rounded-xl flex items-center justify-center transition-all"
                style={{
                  background: query.trim() ? "linear-gradient(135deg, #1b4dff, #7c3aed)" : "rgba(255,255,255,0.05)",
                  color: query.trim() ? "#fff" : "#4b5563",
                  cursor: query.trim() ? "pointer" : "not-allowed",
                  transition: "all 0.2s ease",
                }}
              >
                <ArrowUp size={14} />
              </button>
            )}
          </div>

          {/* Example queries — idle only */}
          {!isActive && (
            <div className="flex flex-wrap gap-2 mt-4 justify-center fade-in">
              {EXAMPLE_QUERIES.map((eq) => (
                <button
                  key={eq}
                  onClick={() => { setQuery(eq); handleSubmit(eq); }}
                  className="px-3 py-1.5 rounded-lg text-xs transition-colors"
                  style={{
                    background: "rgba(255,255,255,0.04)",
                    border: "1px solid rgba(255,255,255,0.06)",
                    color: "#6b7280",
                    fontFamily: "Inter, sans-serif",
                  }}
                  onMouseEnter={e => {
                    (e.currentTarget as HTMLButtonElement).style.color = "#9ca3af";
                    (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(255,255,255,0.12)";
                  }}
                  onMouseLeave={e => {
                    (e.currentTarget as HTMLButtonElement).style.color = "#6b7280";
                    (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(255,255,255,0.06)";
                  }}
                >
                  {eq}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Answer card */}
        {(phase === "thinking" || phase === "streaming" || phase === "done") && (
          <div
            className="w-full mt-6 fade-in"
            style={{ maxWidth: "680px" }}
          >
            {/* Thinking placeholder */}
            {phase === "thinking" && (
              <div
                className="rounded-2xl p-5"
                style={{
                  background: "#111118",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                <div className="flex items-center gap-2 mb-4">
                  <div
                    className="w-5 h-5 rounded-md flex items-center justify-center"
                    style={{ background: "linear-gradient(135deg, #1b4dff, #7c3aed)" }}
                  >
                    <Sparkles size={10} className="text-white" />
                  </div>
                  <span style={{ color: "#4b5563", fontSize: "12px" }}>Arcana is thinking…</span>
                </div>
                {/* Skeleton lines */}
                {[100, 85, 92, 60].map((w, i) => (
                  <div
                    key={i}
                    className="h-3 rounded-full mb-3"
                    style={{
                      width: `${w}%`,
                      background: "linear-gradient(90deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 100%)",
                      backgroundSize: "200% 100%",
                      animation: "shimmer 1.5s ease-in-out infinite",
                      animationDelay: `${i * 0.15}s`,
                    }}
                  />
                ))}
              </div>
            )}

            {/* Streaming / done answer */}
            {(phase === "streaming" || phase === "done") && (
              <div
                className="rounded-2xl overflow-hidden fade-in"
                style={{
                  background: "#111118",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                {/* Answer header */}
                <div
                  className="flex items-center gap-2 px-5 py-3 border-b"
                  style={{ borderColor: "rgba(255,255,255,0.05)" }}
                >
                  <div
                    className="w-5 h-5 rounded-md flex items-center justify-center"
                    style={{ background: "linear-gradient(135deg, #1b4dff, #7c3aed)" }}
                  >
                    <Sparkles size={10} className="text-white" />
                  </div>
                  <span style={{ color: "#6b7280", fontSize: "12px" }}>Answer</span>
                </div>

                {/* Answer body */}
                <div className="px-5 py-4">
                  <div
                    className={phase === "streaming" && !done ? "cursor-blink" : ""}
                    style={{
                      color: "#d1d5db",
                      fontSize: "14px",
                      lineHeight: "1.8",
                      whiteSpace: "pre-line",
                    }}
                  >
                    {displayed}
                  </div>
                </div>

                {/* Sources */}
                {phase === "done" && (
                  <div
                    className="px-5 pb-4 fade-in"
                    style={{ borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "12px" }}
                  >
                    <div style={{ color: "#4b5563", fontSize: "11px", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.06em", fontFamily: "JetBrains Mono, monospace" }}>
                      Sources
                    </div>
                  <div className="flex flex-col gap-8 mb-6">
  
  {/* ==========================================
      1. THE ANSWER SECTION
      ========================================== */}
  {answerData?.answer?.answer && (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <h3 style={{ fontWeight: 600, fontSize: "16px", color: "#f3f4f6" }}>
          Answer
        </h3>
      </div>
      <div style={{ color: "#d1d5db", lineHeight: 1.6, fontSize: "15px" }}>
        {answerData.answer.answer}
      </div>
    </div>
  )}

  {/* ==========================================
      2. THE PLAN SECTION (DAG Arrows)
      ========================================== */}
  {answerData?.metadata?.plan && (
    <div className="flex flex-col gap-3">
      <h3 style={{ fontWeight: 600, fontSize: "14px", color: "#9ca3af", textTransform: "uppercase", letterSpacing: "0.05em" }}>
        Execution Plan
      </h3>
      <div className="flex flex-col gap-2">
        {parseExecutionPlan(answerData.metadata.plan).map((step, index) => (
          <div key={index} className="flex items-center gap-3 text-xs" style={{ fontFamily: "JetBrains Mono, monospace" }}>
            <span className="text-gray-500 w-12">Step {index + 1}</span>
            <div className="flex items-center gap-2 bg-gray-800/50 p-1.5 rounded-md border border-gray-700/50">
              <span className="text-blue-400 px-2 py-0.5 bg-blue-500/10 rounded">
                {step[0]}
              </span>
              <span className="text-gray-500">→</span>
              <span className="text-emerald-400 px-2 py-0.5 bg-emerald-500/10 rounded">
                {step[1]}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )}

  {/* ==========================================
      3. THE CONTEXT SECTION (Collapsible Tools)
      ========================================== */}
  {answerData?.metadata?.context && (
    <div className="flex flex-col gap-3">
      <h3 style={{ fontWeight: 600, fontSize: "14px", color: "#9ca3af", textTransform: "uppercase", letterSpacing: "0.05em" }}>
        Tool Context
      </h3>
      
      <div className="flex flex-col gap-2">
        {parseContextByTool(answerData.metadata.context).map((item, i) => (
          /* Using the native HTML <details> tag for a zero-state collapsible dropdown */
          <details 
            key={i} 
            className="group rounded-lg border border-gray-800 bg-gray-900/40 overflow-hidden"
          >
            <summary className="flex cursor-pointer items-center justify-between p-3 text-sm font-semibold text-gray-300 hover:bg-gray-800 transition-colors list-none">
              <div className="flex items-center gap-3">
                {/* A little indicator to show it's a tool */}
                <span className="flex h-5 w-5 items-center justify-center rounded bg-gray-800 text-gray-400 text-xs">
                  {i + 1}
                </span>
                <span style={{ fontFamily: "JetBrains Mono, monospace", color: "#a5b4fc" }}>
                  {item.tool}
                </span>
              </div>
              
              {/* Dropdown Arrow (Rotates when open via Tailwind group-open class) */}
              <svg 
                className="w-4 h-4 text-gray-500 group-open:rotate-180 transition-transform" 
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </summary>
            
            {/* The collapsible content area */}
            <div className="border-t border-gray-800 p-4 bg-black/20">
              <pre 
                className="text-xs text-gray-400 overflow-x-auto whitespace-pre-wrap" 
                style={{ fontFamily: "JetBrains Mono, monospace", lineHeight: 1.5 }}
              >
                {item.output}
              </pre>
            </div>
          </details>
        ))}
      </div>
    </div>
  )}
</div>
                  </div>
                )}

                {/* Actions */}
                {phase === "done" && (
                  <div
                    className="flex items-center gap-1 px-4 py-2.5 border-t fade-in"
                    style={{ borderColor: "rgba(255,255,255,0.05)" }}
                  >
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-colors"
                      style={{
                        color: copied ? "#34d399" : "#4b5563",
                        fontSize: "11px",
                        background: "transparent",
                      }}
                      onMouseEnter={e => !copied && ((e.currentTarget as HTMLButtonElement).style.color = "#9ca3af")}
                      onMouseLeave={e => !copied && ((e.currentTarget as HTMLButtonElement).style.color = "#4b5563")}
                    >
                      <Copy size={12} />
                      {copied ? "Copied" : "Copy"}
                    </button>
                    <button
                      className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-colors"
                      style={{ color: "#4b5563", fontSize: "11px" }}
                      onMouseEnter={e => ((e.currentTarget as HTMLButtonElement).style.color = "#9ca3af")}
                      onMouseLeave={e => ((e.currentTarget as HTMLButtonElement).style.color = "#4b5563")}
                    >
                      <Share2 size={12} />
                      Share
                    </button>
                    <div className="ml-auto flex items-center gap-1">
                      <button
                        className="p-1.5 rounded-lg transition-colors"
                        style={{ color: "#4b5563" }}
                        onMouseEnter={e => ((e.currentTarget as HTMLButtonElement).style.color = "#34d399")}
                        onMouseLeave={e => ((e.currentTarget as HTMLButtonElement).style.color = "#4b5563")}
                      >
                        <ThumbsUp size={12} />
                      </button>
                      <button
                        className="p-1.5 rounded-lg transition-colors"
                        style={{ color: "#4b5563" }}
                        onMouseEnter={e => ((e.currentTarget as HTMLButtonElement).style.color = "#f87171")}
                        onMouseLeave={e => ((e.currentTarget as HTMLButtonElement).style.color = "#4b5563")}
                      >
                        <ThumbsDown size={12} />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Empty state message */}
        {!isActive && (
          <p
            className="mt-8 text-xs fade-in"
            style={{ color: "#374151", fontFamily: "JetBrains Mono, monospace" }}
          >
            Powered by vector search + cross-encoder reranking
          </p>
        )}
      </main>
    </div>
  );
}
