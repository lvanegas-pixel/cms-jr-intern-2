const API_BASE_URL = 'http://localhost:8000/api'

const errorMessage = document.getElementById('error-message');
const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const projectForm = document.getElementById('project-form');
const projectNameInput = document.getElementById('project_name');
const projectList = document.getElementById('project_list');
const selectedProjectTitle = document.getElementById('selected-project-title');
const assetList = document.getElementById('asset_list');
const logoutBtn = document.getElementById('logout-btn');
const prevProjectsBtn = document.getElementById('prev-projects-btn');
const nextProjectsBtn = document.getElementById('next-projects-btn');
const prevAssetsBtn = document.getElementById('prev-assets-btn');
const nextAssetsBtn = document.getElementById('next-assets-btn');

let authToken = localStorage.getItem('authToken') || '';

let currentProjectsNextUrl = null;
let currentProjectsPrevUrl = null;

let currentSelectedProjectId = null;
let currentSelectedProjectName = '';
let currentAssetsNextUrl = null;
let currentAssetsPrevUrl = null;

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.color = 'red';
    errorMessage.style.fontWeight = 'bold';
}

function clearError() {
    errorMessage.textContent = '';
}

function getHeaders(includeContentType = true) {
    const headers = {};
    if (includeContentType) {
        headers['content-Type'] = 'application/json';
    }
    if (authToken) {
        headers['authorization'] = `Token ${authToken}`;
    }
    return headers;
}

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearError();

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    try {
        const response = await fetch(`${API_BASE_URL}/login/`, {
            method: 'POST',
            headers: getHeaders(true),
            body: JSON.stringify({username, password})
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        authToken = data.token;
        localStorage.setItem('authToken', authToken);

        passwordInput.value = '';
        showError('Login successful! Token has been saved.', true);

        await (fetchProjects());
    } catch (error) {
        showError(error.message);
    }
})

async function fetchProjects(url = `${API_BASE_URL}/projects/`) {
    clearError();
    try {
        const response = await fetch(url, {
            headers: getHeaders(false)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        const projects = data.results || data;

        currentProjectsNextUrl = data.next || null;
        currentProjectsPrevUrl = data.previous || null;

        updateProjectsPaginationUI();
        renderProjects(projects);
    } catch (error) {
        showError(error.message);
        projectList.innerHTML = '<li>Could not load projects.</li>';
        currentProjectsNextUrl = null;
        currentProjectsPrevUrl = null;
        updateProjectsPaginationUI();
    }
}

function updateProjectsPaginationUI() {
    prevProjectsBtn.disabled = !currentProjectsPrevUrl;
    nextProjectsBtn.disabled = !currentProjectsNextUrl;
}

prevProjectsBtn.addEventListener('click', () => {
    if (currentProjectsPrevUrl) {
        fetchProjects(currentProjectsPrevUrl);
    }
});

nextProjectsBtn.addEventListener('click', () => {
    if (currentProjectsNextUrl) {
        fetchProjects(currentProjectsNextUrl);
    }
});

function renderProjects(projects) {
    projectList.innerHTML = '';

    if (!projects || projects.length === 0) {
        projectList.innerHTML = '<li>Empty list.</li>';
        return;
    }

    projects.forEach(project => {
        const li = document.createElement('li');
        li.textContent = project.name;
        li.style.cursor = 'pointer';

        li.addEventListener('click', () => {
            fetchProjectAssets(project.id, project.name);
        });

        projectList.appendChild(li);
    });
}

projectForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearError();

    const name = projectNameInput.value.trim();
    if (!name) return;

    try {
        const response = await fetch(`${API_BASE_URL}/projects/`, {
            method: 'POST',
            headers: getHeaders(true),
            body: JSON.stringify({name})
        });

        if (response.status === 401) {
            throw new Error('No authorization (401). You need to login first.');
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        projectNameInput.value = '';
        await fetchProjects();
    } catch (error) {
        showError(error.message);
    }
});

async function fetchProjectAssets(projectId, projectName, url = null) {
    clearError();

    if (projectId !== undefined && projectId !== null) {
        currentSelectedProjectId = projectId;
        currentSelectedProjectName = projectName;
    }

    selectedProjectTitle.textContent = `Assets of the project: ${projectName}`;
    assetList.innerHTML = '<li>Loading Assets...</li>';

    const targetUrl = url || `${API_BASE_URL}/assets/?project=${currentSelectedProjectId}`

    try {
        const response = await fetch(targetUrl, {
            headers: getHeaders(false)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        const assets = data.results || data;

        currentAssetsNextUrl = data.next || null;
        currentAssetsPrevUrl = data.previous || null;

        updateAssetsPaginationUI();
        renderAssets(assets);
    } catch (error) {
        showError(error.message);
        assetList.innerHTML = '<li>Error from loading Assets.</li>';
        currentAssetsNextUrl = null;
        currentAssetsPrevUrl = null;
        updateAssetsPaginationUI();
    }
}

function updateAssetsPaginationUI() {
    prevAssetsBtn.disabled = !currentAssetsPrevUrl;
    nextAssetsBtn.disabled = !currentAssetsNextUrl;
}

prevAssetsBtn.addEventListener('click', () => {
    if (currentAssetsPrevUrl) {
        fetchProjectAssets(null, null, currentAssetsPrevUrl)
    }
});

nextAssetsBtn.addEventListener('click', () => {
    if (currentAssetsNextUrl) {
        fetchProjectAssets(null, null, currentAssetsNextUrl)
    }
});

function renderAssets(assets) {
    assetList.innerHTML = '';

    if (!assets || assets.length === 0) {
        assetList.innerHTML = '<li>Empty list of assets.</li>';
        return;
    }

    assets.forEach(asset => {
        const li = document.createElement('li');
        li.textContent = asset.name;
        assetList.appendChild(li);
    });
}
function updateAuthUI() {
    if (!authToken) {
        projectList.innerHTML = '<li>Please log in to see projects</li>'
        assetList.innerHTML = '';
        selectedProjectTitle.textContent = 'Select a project to see their assets.';
        currentProjectsNextUrl = null;
        currentProjectsPrevUrl = null;
        currentAssetsNextUrl = null;
        currentAssetsPrevUrl = null;

        updateProjectsPaginationUI();
        updateAssetsPaginationUI();
    }
}

logoutBtn.addEventListener('click', () => {
    authToken= '';
    localStorage.removeItem('authToken');
    showError('Log out successful.', true);
    updateAuthUI()
})

updateAuthUI()
if (authToken) {
    fetchProjects()
}