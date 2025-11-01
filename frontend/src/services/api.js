// Use Vite environment variables (prefixed with VITE_) via import.meta.env.
// Fall back to localhost if not provided.
const API_BASE_URL ="https://verinews-czqj.onrender.com/api/v1";

export const checkNewsText = async (text, language = "en") => {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("language", language);

  console.log("🔍 Sending request to:", `${API_BASE_URL}/news/check-text`);
  const response = await fetch(`${API_BASE_URL}/news/check-text`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze text");
  }

  const data = await response.json();
  console.log("✅ Backend response:", data);
  return data;
};

export const checkNewsVoice = async (audioBlob, language = "en") => {
  const formData = new FormData();
  formData.append("audio_file", audioBlob, "recording.wav");
  formData.append("language", language);

  const response = await fetch(`${API_BASE_URL}/news/check-voice`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze voice input");
  }

  return response.json();
};

export const checkNewsImage = async (imageFile, text = "", language = "en") => {
  const formData = new FormData();
  formData.append("image_file", imageFile);
  formData.append("text", text);
  formData.append("language", language);

  const response = await fetch(`${API_BASE_URL}/news/check-image`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze image");
  }

  return response.json();
};
