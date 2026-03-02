/**
 * NEXUS Frontend — E2E Tests
 * Validates page load, core UI elements, and API connectivity.
 */
import { test, expect } from '@playwright/test';

test.describe('NEXUS Dashboard', () => {
    test('page loads successfully', async ({ page }) => {
        await page.goto('/');
        await expect(page).toHaveTitle(/nexus/i);
    });

    test('main heading is visible', async ({ page }) => {
        await page.goto('/');
        const heading = page.locator('h1').first();
        await expect(heading).toBeVisible();
    });

    test('no console errors on load', async ({ page }) => {
        const errors: string[] = [];
        page.on('console', msg => {
            if (msg.type() === 'error') errors.push(msg.text());
        });
        await page.goto('/');
        await page.waitForLoadState('networkidle');
        expect(errors).toHaveLength(0);
    });
});

test.describe('NEXUS API Integration', () => {
    test('backend health check responds', async ({ request }) => {
        const resp = await request.get('http://localhost:8000/health');
        expect(resp.ok()).toBeTruthy();
        const data = await resp.json();
        expect(data.status).toBe('OPERATIONAL');
    });

    test('command list is available', async ({ request }) => {
        const resp = await request.get('http://localhost:8000/api/commands');
        expect(resp.ok()).toBeTruthy();
        const data = await resp.json();
        expect(data.commands).toContain('SCAN_TODO');
    });
});
