// API Base URL - Leave as empty string "" if using vercel.json rewrites or localhost same-origin.
// If deploying frontend independently on Vercel without rewrites, paste your Railway backend URL here (e.g., "https://fundiq.up.railway.app").
const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    const userInput = document.getElementById("userInput");
    const chatHistory = document.getElementById("chatHistory");
    const typingIndicator = document.getElementById("typingIndicator");
    const welcomeSection = document.getElementById("welcomeSection");
    const btnClearChat = document.getElementById("btnClearChat");
    
    // Modal elements
    const btnToggleSchemes = document.getElementById("btnToggleSchemes");
    const btnCloseSchemes = document.getElementById("btnCloseSchemes");
    const schemesModal = document.getElementById("schemesModal");
    const schemesList = document.getElementById("schemesList");

    const btnToggleSchemesMobile = document.getElementById("btnToggleSchemesMobile");
    const modalBackdrop = document.getElementById("modalBackdrop");

    function openModal() {
        if (schemesModal) {
            schemesModal.classList.remove("hidden");
            schemesModal.classList.add("flex");
            loadSchemes();
        }
    }
    function closeModal() {
        if (schemesModal) {
            schemesModal.classList.add("hidden");
            schemesModal.classList.remove("flex");
        }
    }

    if (btnToggleSchemes) btnToggleSchemes.addEventListener("click", openModal);
    if (btnToggleSchemesMobile) btnToggleSchemesMobile.addEventListener("click", openModal);
    if (btnCloseSchemes) btnCloseSchemes.addEventListener("click", closeModal);
    if (modalBackdrop) modalBackdrop.addEventListener("click", closeModal);
    window.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

    async function loadSchemes() {
        try {
            const res = await fetch(`${API_BASE_URL}/api/schemes`);
            const data = await res.json();
            if (data.schemes && data.schemes.length > 0) {
                schemesList.innerHTML = data.schemes.map(s => `
                    <div class="bg-surface-container-low border border-white/5 p-4 rounded-2xl hover:border-primary/20 transition-all flex flex-col justify-between">
                        <div>
                            <h4 class="text-on-surface font-bold text-base mb-2">${s.name}</h4>
                            <div class="flex items-center gap-2 mb-4">
                                <span class="px-2 py-0.5 rounded ${s.category.toLowerCase().includes('large') ? 'bg-error/10 text-error' : 'bg-secondary/10 text-secondary'} text-[10px] font-bold uppercase">${s.category}</span>
                            </div>
                        </div>
                        <div class="flex justify-between items-center pt-3 border-t border-white/5 text-xs">
                            <a href="${s.official_sid_kim_url}" target="_blank" class="text-primary font-medium flex items-center gap-1 hover:underline">
                                <span class="material-symbols-outlined text-[16px]">description</span> Official SID
                            </a>
                            <a href="${s.groww_url}" target="_blank" class="text-secondary font-medium hover:underline">Groww ↗</a>
                        </div>
                    </div>
                `).join("");
            } else {
                schemesList.innerHTML = "<p class='text-on-surface-variant'>No schemes found in corpus.</p>";
            }
        } catch (err) {
            schemesList.innerHTML = "<p class='text-error'>Failed to load corpus data.</p>";
            console.error(err);
        }
    }

    // Example pill click handlers
    document.querySelectorAll(".pill, .refusal-link").forEach(el => {
        el.addEventListener("click", (e) => {
            e.preventDefault();
            const query = el.getAttribute("data-query");
            if (query) {
                userInput.value = query;
                handleChatSubmit(query);
            }
        });
    });

    // Clear chat
    btnClearChat.addEventListener("click", () => {
        chatHistory.innerHTML = `
            <div class="flex justify-start animate-in fade-in duration-300">
                <div class="glass p-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-xl border border-secondary/20">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-secondary text-base">verified</span>
                        <span class="text-secondary font-bold text-xs uppercase tracking-wider">FundIQ Ready</span>
                    </div>
                    <p class="text-on-surface text-sm leading-relaxed">Chat history cleared. I am ready to answer your factual mutual fund queries for the selected ICICI Prudential schemes.</p>
                </div>
            </div>
        `;
        if (welcomeSection) welcomeSection.style.display = "block";
    });

    // Chat Form Submit
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (query) {
            handleChatSubmit(query);
            userInput.value = "";
        }
    });

    async function handleChatSubmit(query) {
        // Hide welcome hero on first question to give more chat room
        if (welcomeSection) {
            welcomeSection.style.display = "none";
        }

        // Add user message
        appendMessage("user", query, "You");
        
        // Show typing indicator
        typingIndicator.classList.remove("hidden");
        scrollToBottom();

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            typingIndicator.classList.add("hidden");

            if (response.ok) {
                appendAssistantMessage(data);
            } else {
                appendMessage("system", `Error: ${data.detail || "Something went wrong."}`, "System Alert");
            }
        } catch (err) {
            typingIndicator.classList.add("hidden");
            appendMessage("system", "Network error. Please make sure the local server is running.", "Connection Error");
            console.error(err);
        }
        scrollToBottom();
    }

    function appendMessage(sender, text, name) {
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const msgDiv = document.createElement("div");
        
        if (sender === 'user') {
            msgDiv.className = "flex justify-end animate-in slide-in-from-right-4 duration-300";
            msgDiv.innerHTML = `
                <div class="bg-primary-container text-on-primary-container px-4 py-3 rounded-2xl rounded-tr-sm font-body-md max-w-[85%] shadow-lg inner-glow-primary">
                    <p class="text-sm md:text-base leading-relaxed">${escapeHtml(text)}</p>
                    <span class="block text-[10px] text-right opacity-70 mt-1 font-mono-data">${timeStr}</span>
                </div>
            `;
        } else {
            msgDiv.className = "flex justify-start animate-in slide-in-from-left-4 duration-300";
            msgDiv.innerHTML = `
                <div class="glass p-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-xl border border-error/30 bg-error/5">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-error text-base">error</span>
                        <span class="text-error font-bold text-xs uppercase tracking-wider">${name || 'System Alert'}</span>
                    </div>
                    <p class="text-on-surface text-sm leading-relaxed">${escapeHtml(text)}</p>
                </div>
            `;
        }
        chatHistory.appendChild(msgDiv);
    }

    function appendAssistantMessage(data) {
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const msgDiv = document.createElement("div");
        const isRefused = data.is_refused;
        
        msgDiv.className = "flex justify-start animate-in slide-in-from-left-4 duration-500";
        
        if (isRefused) {
            msgDiv.innerHTML = `
                <div class="bg-tertiary-container/10 border border-tertiary-container/30 p-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-lg">
                    <div class="flex items-start gap-3">
                        <span class="material-symbols-outlined text-tertiary-container text-xl mt-0.5">warning</span>
                        <div>
                            <h4 class="text-tertiary-container font-bold text-base mb-1">Advisory Query Refused (${escapeHtml(data.refusal_reason || 'SEBI Guardrail')})</h4>
                            <p class="text-on-surface-variant text-sm leading-relaxed mb-3">${escapeHtml(data.answer)}</p>
                            <a href="${data.citation_url || 'https://www.amfiindia.com'}" target="_blank" class="inline-flex items-center gap-2 text-primary font-bold text-xs hover:gap-3 transition-all bg-primary/10 px-3 py-1.5 rounded-lg">
                                View AMFI Educational Guides <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
                            </a>
                        </div>
                    </div>
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="glass p-5 rounded-2xl rounded-tl-sm max-w-[90%] shadow-xl border border-secondary/20">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-secondary/10 text-secondary px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-widest flex items-center gap-1">
                            <span class="material-symbols-outlined text-[14px]">verified</span> Verified Answer
                        </span>
                        <div class="h-1 w-1 bg-surface-variant rounded-full"></div>
                        <span class="text-on-surface-variant text-xs font-medium flex items-center gap-1 truncate max-w-[200px] md:max-w-none">
                            <span class="material-symbols-outlined text-[14px]">description</span> ${escapeHtml(data.scheme_referenced || 'Official SID Source')}
                        </span>
                    </div>
                    <p class="text-on-surface text-sm md:text-base leading-relaxed">${escapeHtml(data.answer)}</p>
                    <div class="mt-4 pt-3 border-t border-white/5 flex justify-between items-center flex-wrap gap-2">
                        <span class="text-[11px] font-mono-data text-on-surface-variant/80">${escapeHtml(data.footer || 'Last updated from sources: July 2026')}</span>
                        <a href="${data.citation_url}" target="_blank" class="text-primary text-[11px] font-bold uppercase hover:underline flex items-center gap-1 bg-primary/10 hover:bg-primary/20 transition-colors px-3 py-1.5 rounded-lg">
                            <span class="material-symbols-outlined text-[14px]">open_in_new</span> Official Source Citation
                        </a>
                    </div>
                </div>
            `;
        }
        chatHistory.appendChild(msgDiv);
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return "";
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
