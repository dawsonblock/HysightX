import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";
import { TextDecoder, TextEncoder } from "util";

afterEach(() => {
  cleanup();
});

if (!window.TextEncoder) {
	window.TextEncoder = TextEncoder;
}

if (!globalThis.TextEncoder) {
	globalThis.TextEncoder = TextEncoder;
}

if (!window.TextDecoder) {
	window.TextDecoder = TextDecoder;
}

if (!globalThis.TextDecoder) {
	globalThis.TextDecoder = TextDecoder;
}

if (!window.HTMLElement.prototype.scrollIntoView) {
	window.HTMLElement.prototype.scrollIntoView = vi.fn();
}