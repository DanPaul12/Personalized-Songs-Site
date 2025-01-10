import React, { useEffect, useState } from 'react';
import { getBlogBySlug } from './blogService';
import { useParams } from 'react-router-dom';

const BlogDetails = () => {
  const { slug } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    const fetchBlog = async () => {
      try {
        const data = await getBlogBySlug(slug);
        setBlog(data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchBlog();
  }, [slug]);

  if (!blog) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>{blog.title}</h1>
      <p>By {blog.author} on {new Date(blog.created_at).toLocaleDateString()}</p>
      <p>Category: {blog.category}</p>
      <div dangerouslySetInnerHTML={{ __html: blog.content }} />
    </div>
  );
};

export default BlogDetails;