import { apiGet, apiPost, hostPrefix } from "./request.js";

export async function getTemplateDeployments() {
  return apiGet(`${hostPrefix}/deploy/templates/all`);
}

export async function retryTemplateDeployment(id) {
  return apiPost(`${hostPrefix}/deploy/templates/retry`, { id });
}
