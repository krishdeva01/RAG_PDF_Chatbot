const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Helper function to handle API requests
const fetchApi = async (endpoint, method, body = null, headers = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: body ? JSON.stringify(body) : null,
  };

  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Something went wrong');
  }

  return data;
};

// User Authentication
export const signup = async (username, password) => {
  return fetchApi('/signup', 'POST', { username, password });
};

export const login = async (username, password) => {
  return fetchApi('/login', 'POST', { username, password });
};

// PDF Upload
export const uploadPdf = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to upload PDF');
  }

  return data;
};

// Chat
export const chat = async (message) => {
  return fetchApi('/chat', 'POST', { message }, {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
  });
};