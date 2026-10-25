# Balance-scale Llama diagnostic

    format  calls  valid  changed_features  truncated
      chat      3      3                 3          0
completion      3      0                 0          3

No H&M or heldout result. Executable output alone does not establish useful feature discovery.
Chat/completion differences suggest format sensitivity;3 draws do not establish causality.
If both fail, inspect responses and model configuration before more H&M search.