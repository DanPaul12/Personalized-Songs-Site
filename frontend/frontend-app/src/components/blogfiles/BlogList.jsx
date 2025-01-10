import React, { useEffect, useState } from 'react';
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
      <h1>Blog Posts</h1>
      {blogs.map(blog => (
        <div key={blog.id}>
          <h2><Link to={`/blogs/${blog.slug}`}>{blog.title}</Link></h2>
          <p>{blog.category}</p>
          <p>By {blog.author} on {new Date(blog.created_at).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
};

export default BlogList;