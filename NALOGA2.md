# Featuri/pristopi za identifikacijo (logotipov) strank

- img/svg tagi, fuzzy matching imen css classov (npr. "img.customers-hero_logo")
- matchanje alt-texta z bazo znanih imen podjetij
- image logo classification (npr. z visual modelom, ki je fine-tunan za klasifikacijo logotipov)
- image similarity search z bazo znanih logotipov (npr. fine-tunan image embedding model + pgVector + cosine similarity)
- layout features: koordinate slikovnih elementov
- blizina podobnih elementov (logotipi strank se pogosto pojavljajo v seznamih)
- embedding texta zraven img/svg elementov (npr. za detekcijo "customer story")
- named entity recognition / uporaba LLM-ja za ekstrakcijo imen strank iz teksta na straneh.
- uporaba manjsega fine-tuned modela za direktno konverzijo HTML -> JSON (s pre-defined schemo) (v stilu [ReaderLM-v2](https://huggingface.co/jinaai/ReaderLM-v2))
- "agentic" pristop - uporaba (V)LLM-jev za avtonomno navigiranje po straneh (v stilu [browser-use](https://github.com/browser-use/browser-use) ali [smolagents](https://huggingface.co/docs/smolagents/en/examples/web_browser)) - uporabno za primer ko nismo prepricani, na katerih podstraneh se nahajajo stranke.