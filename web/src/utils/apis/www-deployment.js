import { apiGet, apiPost, hostPrefix } from "./request.js";

export async function getWwwDeployments() {
  return apiGet(`${hostPrefix}/deploy/www/all`);
}

export async function retryWwwDeployment(id) {
  return apiPost(`${hostPrefix}/deploy/www/retry`, { id });
}
