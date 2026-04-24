import "@/App.css";
import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HCAChat from "@/components/HCAChat";
import MemoryBrowser from "@/components/MemoryBrowser";
import OperatorConsole from "@/components/OperatorConsole";
import AutonomyWorkspace from "@/features/autonomy/AutonomyWorkspace";
import { Toaster } from "@/components/ui/toaster";

const SELECTED_RUN_STORAGE_KEY = "hysight:selected-run-id";
const ACTIVE_VIEW_STORAGE_KEY = "hysight:active-view";
const SELECTED_RUN_QUERY_PARAM = "run";
const ACTIVE_VIEW_QUERY_PARAM = "view";

/* ── Inline SVG icon set ─────────────────────────────────────────────────── */
function IconTrendUp({ size = 18, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
      <polyline points="17 6 23 6 23 12" />
    </svg>
  );
}
function IconClock({ size = 18, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}
function IconDatabase({ size = 18, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
    </svg>
  );
}
function IconCpu({ size = 18, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <rect x="9" y="9" width="6" height="6" />
      <line x1="9" y1="1" x2="9" y2="4" /><line x1="15" y1="1" x2="15" y2="4" />
      <line x1="9" y1="20" x2="9" y2="23" /><line x1="15" y1="20" x2="15" y2="23" />
      <line x1="20" y1="9" x2="23" y2="9" /><line x1="20" y1="14" x2="23" y2="14" />
      <line x1="1" y1="9" x2="4" y2="9" /><line x1="1" y1="14" x2="4" y2="14" />
    </svg>
  );
}
function IconShield({ size = 18, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <polyline points="9 12 11 14 15 10" />
    </svg>
  );
}
function IconHome({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}
function IconPlay({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <polygon points="10 8 16 12 10 16 10 8" fill={color} stroke="none" />
    </svg>
  );
}
function IconBrain({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.46 2.5 2.5 0 0 1-1.04-4.89A5 5 0 0 1 4.5 8 5 5 0 0 1 9.5 3" />
      <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.46 2.5 2.5 0 0 0 1.04-4.89A5 5 0 0 0 19.5 8 5 5 0 0 0 14.5 3" />
    </svg>
  );
}
function IconGear({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}
function IconHelpCircle({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}
function IconActivity({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
    </svg>
  );
}
function IconSearch({ size = 14, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}
function IconRefresh({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 4 23 10 17 10" />
      <polyline points="1 20 1 14 7 14" />
      <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
    </svg>
  );
}
function IconBell({ size = 16, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
      <path d="M13.73 21a2 2 0 0 1-3.46 0" />
    </svg>
  );
}
function IconChevronDown({ size = 12, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 12 15 18 9" />
    </svg>
  );
}
function IconExpand({ size = 14, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="15 3 21 3 21 9" />
      <polyline points="9 21 3 21 3 15" />
      <line x1="21" y1="3" x2="14" y2="10" />
      <line x1="3" y1="21" x2="10" y2="14" />
    </svg>
  );
}
function IconX({ size = 14, color = "currentColor" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

const WORKSPACE_VIEWS = [
  { id: "assist",   label: "Assist",   Icon: IconHome },
  { id: "runs",     label: "Runs",     Icon: IconPlay },
  { id: "memory",   label: "Memory",   Icon: IconBrain },
  { id: "autonomy", label: "Autonomy", Icon: IconGear },
];

const BOTTOM_NAV_ITEMS = [
  { id: "settings", label: "Settings", Icon: IconGear },
  { id: "help",     label: "Help",     Icon: IconHelpCircle },
];

function getGreeting() {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}

function isValidWorkspaceView(value) {
  return WORKSPACE_VIEWS.some((v) => v.id === value);
}

function readSelectedRunFromUrl() {
  try { return new URLSearchParams(window.location.search).get(SELECTED_RUN_QUERY_PARAM); }
  catch { return null; }
}

function readStoredSelectedRun() {
  try { return window.localStorage.getItem(SELECTED_RUN_STORAGE_KEY); }
  catch { return null; }
}

function readInitialSelectedRun() {
  return readSelectedRunFromUrl() || readStoredSelectedRun();
}

function readActiveViewFromUrl() {
  try {
    const v = new URLSearchParams(window.location.search).get(ACTIVE_VIEW_QUERY_PARAM);
    return isValidWorkspaceView(v) ? v : null;
  } catch { return null; }
}

function readStoredActiveView() {
  try {
    const v = window.localStorage.getItem(ACTIVE_VIEW_STORAGE_KEY);
    return isValidWorkspaceView(v) ? v : null;
  } catch { return null; }
}

function readInitialActiveView() {
  return readActiveViewFromUrl() || readStoredActiveView() || "assist";
}

function SidebarNav({ activeView, onChange }) {
  return (
    <aside className="shell-sidebar">
      <div className="shell-sidebar__logo">
        <div className="shell-sidebar__logoMark">H</div>
        <span className="shell-sidebar__logoText">HysightX</span>
      </div>

      <nav className="shell-sidebar__nav" aria-label="Main navigation">
        {WORKSPACE_VIEWS.map((view) => {
          const isActive = activeView === view.id;
          return (
            <button
              key={view.id}
              type="button"
              aria-pressed={isActive}
              className={`shell-sidebar__navItem${isActive ? " is-active" : ""}`}
              onClick={() => onChange(view.id)}
            >
              <span className="shell-sidebar__navIcon">
                <view.Icon size={16} color={isActive ? "#1e40af" : "#64748b"} />
              </span>
              <span className="shell-sidebar__navLabel">{view.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="shell-sidebar__bottom">
        {BOTTOM_NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            type="button"
            className="shell-sidebar__navItem"
          >
            <span className="shell-sidebar__navIcon">
              <item.Icon size={16} color="#64748b" />
            </span>
            <span className="shell-sidebar__navLabel">{item.label}</span>
          </button>
        ))}

        <div className="shell-sidebar__sysStatus">
          <div className="shell-sidebar__sysStatusHeader">
            <IconActivity size={12} color="#94a3b8" />
            <span>System Status</span>
            <button type="button" className="shell-sidebar__sysStatusLink">View all</button>
          </div>
          {[
            { label: "API",      status: "Healthy" },
            { label: "Database", status: "Healthy" },
            { label: "Redis",    status: "Healthy" },
            { label: "Storage",  status: "Healthy" },
            { label: "SSE",      status: "Connected" },
          ].map((svc) => (
            <div key={svc.label} className="shell-sidebar__sysStatusRow">
              <span className="shell-sidebar__sysStatusDot shell-sidebar__sysStatusDot--healthy" />
              <span className="shell-sidebar__sysStatusLabel">{svc.label}</span>
              <span className="shell-sidebar__sysStatusValue shell-sidebar__sysStatusValue--healthy">{svc.status}</span>
            </div>
          ))}
        </div>

        <div className="shell-sidebar__version">HysightX v1.0.0</div>
      </div>
    </aside>
  );
}

function TopBar({ selectedRunId, onSearchMemory }) {
  return (
    <header className="shell-topbar">
      <div className="shell-topbar__left">
        <div className="shell-topbar__backendStatus">
          <span className="shell-topbar__statusDot shell-topbar__statusDot--healthy" />
          <span className="shell-topbar__statusLabel">Backend</span>
          <span className="shell-topbar__statusValue shell-topbar__statusValue--healthy">Healthy</span>
        </div>

        <div className="shell-topbar__runPicker">
          {selectedRunId ? (
            <span className="shell-topbar__runValue">{selectedRunId}</span>
          ) : (
            <>
              <span className="shell-topbar__runLabel">Selected Run</span>
              <span className="shell-topbar__runValue shell-topbar__runValue--empty">—</span>
            </>
          )}
          <span className="shell-topbar__runChevron"><IconChevronDown size={12} color="#94a3b8" /></span>
        </div>
      </div>

      <div className="shell-topbar__center">
        <button
          type="button"
          className="shell-topbar__search"
          onClick={onSearchMemory}
          aria-label="Memory search"
        >
          <IconSearch size={14} color="#94a3b8" />
          <span className="shell-topbar__searchPlaceholder">Memory Search</span>
          <kbd className="shell-topbar__searchKbd">⌘K</kbd>
        </button>
      </div>

      <div className="shell-topbar__right">
        <button type="button" className="shell-topbar__iconBtn" aria-label="Refresh">
          <IconRefresh size={15} color="#64748b" />
        </button>
        <button type="button" className="shell-topbar__iconBtn" aria-label="Notifications">
          <IconBell size={15} color="#64748b" />
          <span className="shell-topbar__badge">3</span>
        </button>
        <div className="shell-topbar__avatar">AD</div>
        <button type="button" className="shell-topbar__userMenu">
          Admin <IconChevronDown size={12} color="#64748b" />
        </button>
      </div>
    </header>
  );
}

function AssistantPanel({ open, onClose, onRunObserved }) {
  if (!open) return null;
  return (
    <aside className="shell-assistant">
      <div className="shell-assistant__header">
        <div className="shell-assistant__titleRow">
          <div className="shell-assistant__avatarMark">H</div>
          <div>
            <div className="shell-assistant__title">HysightX Assistant</div>
            <div className="shell-assistant__online">Online</div>
          </div>
        </div>
        <div className="shell-assistant__actions">
          <button type="button" className="shell-assistant__iconBtn" aria-label="Expand"><IconExpand size={14} /></button>
          <button type="button" className="shell-assistant__iconBtn" aria-label="Close" onClick={onClose}><IconX size={14} /></button>
        </div>
      </div>
      <div className="shell-assistant__body">
        <HCAChat
          memPanelOpen={false}
          onToggleMemPanel={() => {}}
          onRunObserved={onRunObserved}
        />
      </div>
    </aside>
  );
}

function DashboardHome({ selectedRunId, onSelectRun, onRunObserved, operatorRefreshToken, onChangeView }) {
  return (
    <div className="dashboard">
      <div className="dashboard__greeting">
        <h1 className="dashboard__greetingTitle">{getGreeting()}, Admin</h1>
        <p className="dashboard__greetingSubtitle">Here's what's happening across your system.</p>
      </div>

      <div className="dashboard__demoNotice">
        Sample data — connect the backend to see live values
      </div>

      <div className="dashboard__statGrid">
        <div className="dashboard__statCard">
          <div className="dashboard__statIcon dashboard__statIcon--blue">
            <IconTrendUp size={20} color="#3b82f6" />
          </div>
          <div className="dashboard__statBody">
            <div className="dashboard__statLabel">Active Runs</div>
            <div className="dashboard__statValue">8 <span className="dashboard__statDelta dashboard__statDelta--up">+2</span></div>
            <div className="dashboard__statMeta">vs yesterday</div>
          </div>
        </div>
        <div className="dashboard__statCard">
          <div className="dashboard__statIcon dashboard__statIcon--orange">
            <IconClock size={20} color="#f97316" />
          </div>
          <div className="dashboard__statBody">
            <div className="dashboard__statLabel">Pending Approvals</div>
            <div className="dashboard__statValue">3 <span className="dashboard__statDelta dashboard__statDelta--down">-1</span></div>
            <div className="dashboard__statMeta">vs yesterday</div>
          </div>
        </div>
        <div className="dashboard__statCard">
          <div className="dashboard__statIcon dashboard__statIcon--purple">
            <IconDatabase size={20} color="#8b5cf6" />
          </div>
          <div className="dashboard__statBody">
            <div className="dashboard__statLabel">Memories</div>
            <div className="dashboard__statValue">1,248 <span className="dashboard__statDelta dashboard__statDelta--up">+86</span></div>
            <div className="dashboard__statMeta">vs yesterday</div>
          </div>
        </div>
        <div className="dashboard__statCard">
          <div className="dashboard__statIcon dashboard__statIcon--teal">
            <IconCpu size={20} color="#0d9488" />
          </div>
          <div className="dashboard__statBody">
            <div className="dashboard__statLabel">Autonomy Agents</div>
            <div className="dashboard__statValue">6 <span className="dashboard__statBadge dashboard__statBadge--online">Online</span></div>
            <div className="dashboard__statMeta dashboard__statMeta--warn">2 Degraded</div>
          </div>
        </div>
        <div className="dashboard__statCard">
          <div className="dashboard__statIcon dashboard__statIcon--green">
            <IconShield size={20} color="#16a34a" />
          </div>
          <div className="dashboard__statBody">
            <div className="dashboard__statLabel">System Health</div>
            <div className="dashboard__statValue">98% <span className="dashboard__statBadge dashboard__statBadge--healthy">Healthy</span></div>
            <div className="dashboard__statMeta">All systems operational</div>
          </div>
        </div>
      </div>

      <div className="dashboard__panels">
        <div className="dashboard__panelLeft">
          <div className="dashboard__card">
            <div className="dashboard__cardHeader">
              <span className="dashboard__cardTitle">Recent Runs</span>
              <button type="button" className="dashboard__cardLink" onClick={() => onChangeView("runs")}>View all</button>
            </div>
            <div className="dashboard__runList">
              {[
                { id: "RUN-2025-05-19-0001", state: "completed",         time: "May 19, 2025 10:24 AM", dur: "12m 42s" },
                { id: "RUN-2025-05-19-0000", state: "awaiting_approval", time: "May 19, 2025 09:41 AM", dur: "18m 7s" },
                { id: "RUN-2025-05-18-9999", state: "completed",         time: "May 18, 2025 04:15 PM", dur: "9m 33s" },
                { id: "RUN-2025-05-18-9998", state: "failed",            time: "May 18, 2025 02:22 PM", dur: "3m 11s" },
                { id: "RUN-2025-05-18-9997", state: "completed",         time: "May 18, 2025 11:03 AM", dur: "14m 55s" },
              ].map((run) => (
                <button
                  key={run.id}
                  type="button"
                  className={`dashboard__runRow${selectedRunId === run.id ? " is-selected" : ""}`}
                  onClick={() => { onSelectRun(run.id); onChangeView("runs"); }}
                >
                  <div className="dashboard__runInfo">
                    <span className={`dashboard__runDot dashboard__runDot--${run.state}`} />
                    <span className="dashboard__runId dashboard__runId--mono">{run.id}</span>
                  </div>
                  <div className="dashboard__runRight">
                    <span className="dashboard__runTime">{run.time}</span>
                    <span className={`dashboard__runBadge dashboard__runBadge--${run.state}`}>
                      {run.state === "awaiting_approval" ? "Awaiting" : run.state === "completed" ? "Completed" : "Failed"}
                    </span>
                    <span className="dashboard__runDur">{run.dur}</span>
                  </div>
                </button>
              ))}
            </div>
            <div className="dashboard__cardFooter">
              Showing 5 of 128 runs
              <button type="button" className="dashboard__cardLink" onClick={() => onChangeView("runs")}>View all runs →</button>
            </div>
          </div>
        </div>

        <div className="dashboard__panelCenter">
          <div className="dashboard__card">
            <div className="dashboard__cardHeader">
              <span className="dashboard__cardTitle">Run Overview</span>
              <span className="dashboard__completedBadge">Completed</span>
              <button type="button" className="dashboard__cardIconBtn">⋮</button>
            </div>
            {selectedRunId ? (
              <div className="dashboard__runOverviewEmbed">
                <OperatorConsole
                  selectedRunId={selectedRunId}
                  onSelectRun={onSelectRun}
                  refreshToken={operatorRefreshToken}
                  onRunObserved={onRunObserved}
                />
              </div>
            ) : (
              <div className="dashboard__runOverviewEmpty">
                <p>Select a run from Recent Runs to see details.</p>
                <button type="button" className="dashboard__cardLink" onClick={() => onChangeView("runs")}>Open Runs workspace</button>
              </div>
            )}
          </div>
        </div>

        <div className="dashboard__panelRight">
          <div className="dashboard__card">
            <div className="dashboard__cardHeader">
              <span className="dashboard__cardTitle">System Activity</span>
              <button type="button" className="dashboard__cardLink">View all</button>
            </div>
            <div className="dashboard__activityList">
              {[
                { sym: "✓", color: "green",  label: "Run completed",      desc: "RUN-2025-05-19-0001 completed successfully.", time: "2m ago" },
                { sym: "↑", color: "blue",   label: "Approval granted",   desc: "Data access request approved by Admin.", time: "8m ago" },
                { sym: "◎", color: "purple", label: "New memory created",  desc: "Customer churn analysis insights stored.", time: "15m ago" },
                { sym: "▷", color: "teal",   label: "Agent started",      desc: "DataAnalyst agent started by system.", time: "16m ago" },
                { sym: "✕", color: "red",    label: "Run failed",         desc: "RUN-2025-05-18-9998 failed during execution.", time: "2h ago" },
              ].map((item, i) => (
                <div key={i} className="dashboard__activityItem">
                  <span className={`dashboard__activityIcon dashboard__activityIcon--${item.color}`}>{item.sym}</span>
                  <div className="dashboard__activityBody">
                    <div className="dashboard__activityLabel">{item.label}</div>
                    <div className="dashboard__activityDesc">{item.desc}</div>
                  </div>
                  <div className="dashboard__activityTime">{item.time}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="dashboard__card dashboard__card--runDist">
            <div className="dashboard__cardHeader">
              <span className="dashboard__cardTitle">Run Status Distribution</span>
              <button type="button" className="dashboard__cardLink">View all</button>
            </div>
            <div className="dashboard__distRow">
              <div className="dashboard__distDonut">
                <svg viewBox="0 0 36 36" className="dashboard__donutSvg">
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#e2e8f0" strokeWidth="3.2" />
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#22c55e" strokeWidth="3.2"
                    strokeDasharray="61 39" strokeDashoffset="25" />
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#3b82f6" strokeWidth="3.2"
                    strokeDasharray="6 94" strokeDashoffset="-36" />
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#f59e0b" strokeWidth="3.2"
                    strokeDasharray="13 87" strokeDashoffset="-42" />
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#94a3b8" strokeWidth="3.2"
                    strokeDasharray="9 91" strokeDashoffset="-55" />
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#ef4444" strokeWidth="3.2"
                    strokeDasharray="11 89" strokeDashoffset="-64" />
                  <text x="18" y="19" textAnchor="middle" fontSize="6" fontWeight="700" fill="#10233c">128</text>
                  <text x="18" y="24" textAnchor="middle" fontSize="3.5" fill="#64748b">Total Runs</text>
                </svg>
              </div>
              <div className="dashboard__distLegend">
                {[
                  { color: "#22c55e", label: "Completed",        pct: "78 (61%)" },
                  { color: "#3b82f6", label: "Running",          pct: "8 (6%)" },
                  { color: "#f59e0b", label: "Awaiting Approval",pct: "16 (13%)" },
                  { color: "#94a3b8", label: "Staled",           pct: "12 (9%)" },
                  { color: "#ef4444", label: "Cancelled",        pct: "14 (11%)" },
                ].map((item) => (
                  <div key={item.label} className="dashboard__distItem">
                    <span className="dashboard__distDot" style={{ background: item.color }} />
                    <span className="dashboard__distLabel">{item.label}</span>
                    <span className="dashboard__distPct">{item.pct}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard__autonomyRow">
        <div className="dashboard__card dashboard__card--autonomy">
          <div className="dashboard__cardHeader">
            <span className="dashboard__cardTitle">Autonomy Overview</span>
            <button type="button" className="dashboard__cardLink" onClick={() => onChangeView("autonomy")}>View all agents</button>
          </div>
          <div className="dashboard__autonomyGrid">
            <div className="dashboard__autonomyStat">
              <div className="dashboard__autonomyStatLabel">Agent Status</div>
              <div className="dashboard__autonomyDonutWrap">
                <svg viewBox="0 0 36 36" className="dashboard__autonomyDonut">
                  <circle cx="18" cy="18" r="13" fill="none" stroke="#e2e8f0" strokeWidth="4" />
                  <circle cx="18" cy="18" r="13" fill="none" stroke="#22c55e" strokeWidth="4"
                    strokeDasharray="33 67" strokeDashoffset="25" />
                  <circle cx="18" cy="18" r="13" fill="none" stroke="#f59e0b" strokeWidth="4"
                    strokeDasharray="16 84" strokeDashoffset="-8" />
                  <text x="18" y="21" textAnchor="middle" fontSize="7" fontWeight="700" fill="#10233c">6</text>
                  <text x="18" y="26" textAnchor="middle" fontSize="3" fill="#64748b">Total</text>
                </svg>
                <div className="dashboard__autonomyAgentLegend">
                  <span className="dashboard__agentLegendDot" style={{ background: "#22c55e" }} /> 4 Online
                  <span className="dashboard__agentLegendDot" style={{ background: "#f59e0b", marginLeft: 8 }} /> 2 Degraded
                  <span className="dashboard__agentLegendDot" style={{ background: "#ef4444", marginLeft: 8 }} /> 0 Offline
                </div>
              </div>
            </div>
            <div className="dashboard__autonomyStat">
              <div className="dashboard__autonomyStatLabel">Budget Status</div>
              <div className="dashboard__autonomyBudget">
                <div className="dashboard__budgetAmount">$2,847 / $5,000</div>
                <div className="dashboard__budgetBar">
                  <div className="dashboard__budgetFill" style={{ width: "57%" }} />
                </div>
                <div className="dashboard__budgetMeta">57%</div>
                <div className="dashboard__budgetSub">Daily budget usage</div>
                <div className="dashboard__budgetReset">Resets in 6h 23m</div>
              </div>
            </div>
            <div className="dashboard__autonomyStat">
              <div className="dashboard__autonomyStatLabel">Pending Escalations</div>
              <div className="dashboard__escalationCount">2</div>
              <div className="dashboard__escalationSub">Requires attention</div>
              <button type="button" className="dashboard__escalationBtn" onClick={() => onChangeView("autonomy")}>
                View Escalations
              </button>
            </div>
            <div className="dashboard__autonomyStat">
              <div className="dashboard__autonomyStatLabel">Kill Switch</div>
              <button type="button" className="dashboard__killSwitchBtn">
                ACTIVATE KILL SWITCH
              </button>
              <div className="dashboard__killSwitchNote">This will stop all autonomous agents immediately.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [assistantOpen, setAssistantOpen] = useState(true);
  const [memOpen, setMemOpen] = useState(false);
  const [selectedRunId, setSelectedRunId] = useState(readInitialSelectedRun);
  const [activeView, setActiveView] = useState(readInitialActiveView);
  const [operatorRefreshToken, setOperatorRefreshToken] = useState(0);

  useEffect(() => {
    try {
      if (selectedRunId) {
        window.localStorage.setItem(SELECTED_RUN_STORAGE_KEY, selectedRunId);
      } else {
        window.localStorage.removeItem(SELECTED_RUN_STORAGE_KEY);
      }
      window.localStorage.setItem(ACTIVE_VIEW_STORAGE_KEY, activeView);

      const params = new URLSearchParams(window.location.search);
      if (selectedRunId) { params.set(SELECTED_RUN_QUERY_PARAM, selectedRunId); }
      else { params.delete(SELECTED_RUN_QUERY_PARAM); }
      if (activeView === "assist") { params.delete(ACTIVE_VIEW_QUERY_PARAM); }
      else { params.set(ACTIVE_VIEW_QUERY_PARAM, activeView); }

      const query = params.toString();
      const nextUrl = `${window.location.pathname}${query ? `?${query}` : ""}${window.location.hash}`;
      window.history.replaceState(window.history.state, "", nextUrl);
    } catch { /* ignore */ }
  }, [activeView, selectedRunId]);

  useEffect(() => {
    const handlePopState = () => {
      setSelectedRunId(readInitialSelectedRun());
      setActiveView(readInitialActiveView());
    };
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const handleSelectRun = (runId) => {
    setSelectedRunId(runId);
    if (runId && runId === selectedRunId) {
      setOperatorRefreshToken((v) => v + 1);
    }
  };

  const handleRunObserved = (runId) => {
    if (!runId) return;
    setSelectedRunId(runId);
    setOperatorRefreshToken((v) => v + 1);
  };

  const handleChangeView = (nextView) => {
    setActiveView(nextView);
    if (nextView === "memory") setMemOpen(false);
  };

  const handleOpenRunFromAutonomy = (runId) => {
    handleSelectRun(runId);
    setActiveView("runs");
  };

  const renderMainContent = () => {
    if (activeView === "assist") {
      return (
        <DashboardHome
          selectedRunId={selectedRunId}
          onSelectRun={handleSelectRun}
          onRunObserved={handleRunObserved}
          operatorRefreshToken={operatorRefreshToken}
          onChangeView={handleChangeView}
        />
      );
    }

    if (activeView === "runs") {
      return (
        <div className="workspace-full">
          <OperatorConsole
            selectedRunId={selectedRunId}
            onSelectRun={handleSelectRun}
            refreshToken={operatorRefreshToken}
            onRunObserved={handleRunObserved}
          />
        </div>
      );
    }

    if (activeView === "memory") {
      return (
        <div className="workspace-full">
          <MemoryBrowser
            open
            title="Memory workspace"
            subtitle="Search, inspect, and clean up retained context."
            variant="embedded"
          />
        </div>
      );
    }

    if (activeView === "autonomy") {
      return (
        <div className="workspace-full">
          <AutonomyWorkspace
            onOpenRun={handleOpenRunFromAutonomy}
            selectedRunId={selectedRunId}
          />
        </div>
      );
    }

    return null;
  };

  return (
    <BrowserRouter>
      <div className="app-root">
        <SidebarNav activeView={activeView} onChange={handleChangeView} />

        <div className="app-main">
          <TopBar
            selectedRunId={selectedRunId}
            onSearchMemory={() => setMemOpen(true)}
          />

          <div className="app-body">
            <div className={`app-content${activeView !== "assist" ? " app-content--workspace" : ""}`}>
              <Routes>
                <Route path="/" element={renderMainContent()} />
              </Routes>
            </div>

            <AssistantPanel
              open={assistantOpen}
              onClose={() => setAssistantOpen(false)}
              onRunObserved={handleRunObserved}
            />
          </div>
        </div>

        {activeView !== "memory" && (
          <MemoryBrowser open={memOpen} onClose={() => setMemOpen(false)} />
        )}
        <Toaster />
      </div>
    </BrowserRouter>
  );
}

export default App;
