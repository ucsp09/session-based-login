const state = {
    resources: []
  };
  
  // -----------------------------
  // Render
  // -----------------------------
  function displayResourcesTable() {
    const resourcesTable = document.getElementById("resourcesTable");
  
    let resourcesTableHtml = `
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Properties</th>
          </tr>
        </thead>
        <tbody>
    `;
  
    for (const resource of state.resources) {
      resourcesTableHtml += `
        <tr>
          <td>${resource.name}</td>
          <td>${formatProperties(resource.properties)}</td>
        </tr>
      `;
    }
  
    resourcesTableHtml += `
        </tbody>
      </table>
    `;
  
    resourcesTable.innerHTML = resourcesTableHtml;
  }
  
  // -----------------------------
  // Helpers
  // -----------------------------
  function formatProperties(properties) {
    if (!properties || typeof properties !== "object") {
      return "";
    }
  
    return Object.entries(properties)
      .map(
        ([key, value]) =>
          `<div><strong>${key}</strong>: ${value}</div>`
      )
      .join("");
  }
  
  // -----------------------------
  // API
  // -----------------------------
  async function callBackendGetAllResourcesAPI() {
    const url = "http://localhost:8000/api/v1/resources";
    return fetch(url, {
      method: "GET",
      credentials: "include"
    });
  }
  
  async function getAllResources() {
    const response = await callBackendGetAllResourcesAPI();
  
    if (!response.ok) {
      console.error("Failed to fetch resources");
      return null;
    }
  
    const data = await response.json();
    return data?.items ?? [];
  }
  
  // -----------------------------
  // State Update
  // -----------------------------
  async function updateResourceTableState() {
    const items = await getAllResources();
  
    if (items !== null) {
      state.resources = items;
      displayResourcesTable();
    }
  }
  
  // -----------------------------
  // Init + Polling
  // -----------------------------
  let polling = true;
  
  async function startUpdatingResourceTableState() {
    // initial load
    await updateResourceTableState();
  
    // polling loop
    while (polling) {
      await new Promise(resolve => setTimeout(resolve, 10000));
      await updateResourceTableState();
    }
  }
  
  // Start AFTER everything is defined
  startUpdatingResourceTableState();
  