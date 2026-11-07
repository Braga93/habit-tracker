import { demoApi } from './demo.js';
import { remoteApi } from './remote.js';

export const isDemo = import.meta.env.VITE_DEMO === 'true';

export const api = isDemo ? demoApi : remoteApi;

export { ApiError } from './errors.js';
export { readToken, saveToken } from './token.js';
