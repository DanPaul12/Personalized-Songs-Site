import React, { useEffect, useState } from 'react';
import { getBlogBySlug } from './blogService';
import { useParams } from 'react-router-dom';
import { Helmet } from "react-helmet";

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

  const truncatedContent = blog.content.slice(0, 150);
  const tagList = blog.tags.join(", ");
  const metaDescription = `${truncatedContent}... Read more about ${blog.category} and topics like ${tagList}.`;

  return (
    <div>
      <Helmet>
        <title>{blog.title} | Dan & Drum Blog</title>
        <meta name="description" content={metaDescription} />
        <meta name="keywords" content={blog.tags.join(", ")} />
      </Helmet>
      <h1>{blog.title}</h1>
      <p>By {blog.author} on {new Date(blog.created_at).toLocaleDateString()}</p>
      <p>Category: {blog.category}</p>
      <div dangerouslySetInnerHTML={{ __html: blog.content }} />
    </div>
  );
};

export default BlogDetails;