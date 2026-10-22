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

let authToken = localStorage.getItem('authToken') || '';

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

async function fetchProjects() {
    clearError();
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`, {
            headers: getHeaders(false)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        const projects = data.results || data;
        renderProjects(projects);
    } catch (error) {
        showError(error.message);
        projectList.innerHTML = '<li>Could not load projects.</li>';
    }
}

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

async function fetchProjectAssets(projectId, projectName) {
    clearError();
    selectedProjectTitle.textContent = `Assets of the project: ${projectName}`;
    assetList.innerHTML = '<li>Loading Assets...</li>';

    try {
        const response = await fetch(`${API_BASE_URL}/assets/`, {
            headers: getHeaders(false)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        const allAssets = data.results || data;
        const projectAssets = allAssets.filter(asset => asset.project_id === projectId);
        renderAssets(projectAssets);
    } catch (error) {
        showError(error.message);
        assetList.innerHTML = '<li>Error from loading Assets.</li>';
    }
}

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