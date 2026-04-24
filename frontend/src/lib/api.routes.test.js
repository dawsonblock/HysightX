/**
 * Route contract regression tests.
 * Asserts that the four run-detail API helpers call /api/hca/run/...
 * and NOT the stale /api/runs/... paths.
 */
import { describe, it, expect, vi, afterEach } from "vitest";

const RUN_ID = "run-regression-001";
const ARTIFACT_ID = "artifact-regression-001";

async function loadApi() {
  vi.resetModules();
  // Stub fetch so no real network call is made
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({}),
    headers: { get: () => "application/json" },
  });
  return import("./api.js");
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("api.js route contracts", () => {
  it("getRunSummary calls /api/hca/run/{id}", async () => {
    const { getRunSummary } = await loadApi();
    await getRunSummary(RUN_ID).catch(() => {});
    const url = global.fetch.mock.calls[0]?.[0];
    expect(url).toContain("/api/hca/run/");
    expect(url).toContain(RUN_ID);
    expect(url).not.toContain("/api/runs/");
  });

  it("listRunEvents calls /api/hca/run/{id}/events", async () => {
    const { listRunEvents } = await loadApi();
    await listRunEvents(RUN_ID, { limit: 10 }).catch(() => {});
    const url = global.fetch.mock.calls[0]?.[0];
    expect(url).toContain("/api/hca/run/");
    expect(url).toContain("/events");
    expect(url).not.toContain("/api/runs/");
  });

  it("listRunArtifacts calls /api/hca/run/{id}/artifacts", async () => {
    const { listRunArtifacts } = await loadApi();
    await listRunArtifacts(RUN_ID, { limit: 10 }).catch(() => {});
    const url = global.fetch.mock.calls[0]?.[0];
    expect(url).toContain("/api/hca/run/");
    expect(url).toContain("/artifacts");
    expect(url).not.toContain("/api/runs/");
  });

  it("getRunArtifactDetail calls /api/hca/run/{id}/artifacts/{artifactId}", async () => {
    const { getRunArtifactDetail } = await loadApi();
    await getRunArtifactDetail(RUN_ID, ARTIFACT_ID).catch(() => {});
    const url = global.fetch.mock.calls[0]?.[0];
    expect(url).toContain("/api/hca/run/");
    expect(url).toContain("/artifacts/");
    expect(url).toContain(ARTIFACT_ID);
    expect(url).not.toContain("/api/runs/");
  });
});
