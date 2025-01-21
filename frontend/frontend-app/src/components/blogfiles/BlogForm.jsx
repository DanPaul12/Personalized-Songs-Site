import React, { useState } from 'react';
import { createBlog, updateBlog } from './blogService';

const BlogForm = ({ existingBlog = null }) => {
  const [formData, setFormData] = useState({
    title: existingBlog?.title || '',
    slug: existingBlog?.slug || '',
    content: existingBlog?.content || '',
    category: existingBlog?.category || '',
    tags: existingBlog?.tags || [],
    author: existingBlog?.author || '', // New field
    imageUrl: existingBlog?.imageUrl || '', // New field
    published: existingBlog?.published || false,
  });

  const [message, setMessage] = useState(''); // For displaying success or error messages

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (existingBlog) {
        await updateBlog(existingBlog.id, formData);
        setMessage('Blog updated successfully!');
      } else {
        await createBlog(formData);
        setMessage('Blog created successfully!');
        setFormData({ // Clear the form after submission
          title: '',
          slug: '',
          content: '',
          category: '',
          tags: [],
          author: '',
          imageUrl: '',
          published: false,
        });
      }
    } catch (err) {
      console.error(err);
      setMessage('An error occurred while submitting the blog.');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Title:
          <input type="text" name="title" value={formData.title} onChange={handleChange} required />
        </label>
        <label>
          Slug:
          <input type="text" name="slug" value={formData.slug} onChange={handleChange} required />
        </label>
        <label>
          Content:
          <textarea name="content" value={formData.content} onChange={handleChange} required />
        </label>
        <label>
          Category:
          <input type="text" name="category" value={formData.category} onChange={handleChange} required />
        </label>
        <label>
          Tags (comma-separated):
          <input
            type="text"
            name="tags"
            value={formData.tags.join(',')}
            onChange={(e) => setFormData({ ...formData, tags: e.target.value.split(',') })}
          />
        </label>
        <label>
          Author:
          <input type="text" name="author" value={formData.author} onChange={handleChange} />
        </label>
        <label>
          Image URL:
          <input type="text" name="imageUrl" value={formData.imageUrl} onChange={handleChange} />
        </label>
        <label>
          Published:
          <input type="checkbox" name="published" checked={formData.published} onChange={handleChange} />
        </label>
        <button type="submit">{existingBlog ? 'Update' : 'Create'} Blog</button>
      </form>
      {message && <p>{message}</p>} {/* Display success/error messages */}
    </div>
  );
};

export default BlogForm;