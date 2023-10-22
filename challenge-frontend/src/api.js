const API_URL = 'http://localhost:8000';

export async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    const result = await response.json();

    if (response.ok) {
      showAlert('File uploaded successfully!', 'success');
    } else {
      showAlert(result.message || 'Failed to upload file', 'error');
    }
  } catch (error) {
    showAlert('An error occurred while uploading the file', 'error');
  }
}

export async function fetchFileInfo() {
  try {
    const response = await fetch(`${API_URL}/file-info`);
    const result = await response.json();

    if (response.ok) {
      showAlert(`File Name: ${result.fileName}, File Merkle Root: ${result.merkle_root}`, 'success');
    } else {
      showAlert(result.message || 'Failed to fetch file info', 'error');
    }
  } catch (error) {
    showAlert('An error occurred while fetching file info', 'error');
  }
}

function showAlert(message, type) {
  const responseDiv = document.getElementById('response');
  responseDiv.innerText = message;
  responseDiv.style.color = type === 'error' ? 'red' : 'green';
}
