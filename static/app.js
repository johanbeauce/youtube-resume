function app() {
  return {
    videoId: '',
    languages: 'en',
    translate: 'en',
    summary: '',
    error: '',
    loading: false,

    get parsedSummary() {
      return marked.parse(this.summary || '');
    },

    async summarize() {
        this.summary = '';
        this.error = '';

        if (!this.videoId.trim()) {
            this.error = "Please enter at least one video ID.";
            return;
        }

        this.loading = true;

        try {
            const response = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                video_ids: [this.videoId],
                languages: this.languages.split(' '),
                translate: this.translate
            })
            });

            const result = await response.json();

            if (result.error) {
            this.error = result.error;
            } else {
            this.summary = result[this.videoId]?.summary || '';
            this.error = result[this.videoId]?.error || '';
            }

        } catch (e) {
            this.error = "Could not connect to the backend.";
        } finally {
            this.loading = false;
        }
    }
}}