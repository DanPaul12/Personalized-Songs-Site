import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api/blogs';

export const getAllBlogs = async () => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

export const getBlogBySlug = async (slug) => {
  const response = await fetch(`http://127.0.0.1:5000/api/blogs/${slug}`);
  if (!response.ok) {
    throw new Error('Failed to fetch blog');
  }
  return response.json();
};

export const createBlog = async (blogData) => {
  const response = await axios.post(API_BASE_URL, blogData);
  return response.data;
};

export const updateBlog = async (id, blogData) => {
  const response = await axios.put(`${API_BASE_URL}/${id}`, blogData);
  return response.data;
};

export const deleteBlog = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/${id}`);
  return response.data;
};