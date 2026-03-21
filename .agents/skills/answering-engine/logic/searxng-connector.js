/**
 * SearxNG Connector Logic
 */
export const searchSearxng = async (query, searxngURL) => {
  const url = new URL(`${searxngURL}/search?format=json`);
  url.searchParams.append('q', query);

  const res = await fetch(url);
  if (!res.ok) throw new Error(`SearXNG error: ${res.statusText}`);

  const data = await res.json();
  return { 
    results: data.results.map(r => ({
      title: r.title,
      url: r.url,
      content: r.content,
      source: r.engine
    })), 
    suggestions: data.suggestions 
  };
};
