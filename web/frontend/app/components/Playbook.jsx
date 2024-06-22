import { useState, useEffect } from 'react';

function PlaybookViewer({ playbookStream }) {
  const [playbookContent, setPlaybookContent] = useState('');

  useEffect(() => {
    async function fetchPlaybookContent() {
      const response = await fetch(playbookStream);
      const reader = response.body.getReader();

      let content = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        content += new TextDecoder().decode(value);
      }

      setPlaybookContent(content);
    }

    fetchPlaybookContent();
  }, [playbookStream]);

  return (
    <div>
      <pre>{playbookContent}</pre>
    </div>
  );
}

export default PlaybookViewer;