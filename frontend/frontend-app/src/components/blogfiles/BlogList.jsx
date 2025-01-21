import React, { useEffect, useState } from 'react';
import './BlogList.css'
import { getAllBlogs } from './blogService'
import { Link } from 'react-router-dom';

const BlogList = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    const fetchBlogs = async () => {
      const data = await getAllBlogs();
      setBlogs(data);
    };

    fetchBlogs();
  }, []);

  return (
    <div>
      <div className="blog-list-container">
        <h1>Blog Posts</h1>
        <div className="blog-cards">
          {blogs.map(blog => (
            <div key={blog.id} className="blog-card">
              <img src={blog.imageUrl} alt={blog.title} className="blog-card-image" />
              <h2><Link to={`/personalized-songs-blogs/${blog.slug}`}>{blog.title}</Link></h2>
              <p>{blog.category}</p>
              <p>By {blog.author} on {new Date(blog.created_at).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BlogList;