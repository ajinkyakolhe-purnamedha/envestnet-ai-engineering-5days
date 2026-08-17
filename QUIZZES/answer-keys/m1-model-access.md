# M1 answer key

1. A — A model produces outputs from inputs.
2. A — A product needs surrounding application behavior.
3. A — Hosted models are accessed through a service/API.
4. A — Local models run on controlled hardware.
5. A — Hosted access reduces operations but adds dependency and cost.
6. A — Local access increases control but adds operational work.
7. A — Selection follows the task and operating requirements.
8. A — A boundary hides provider-specific details.
9. A — Secrets belong in protected configuration.
10. A — Empty output needs safe handling and observability.
11. It prevents a call when required configuration is missing.
12. Extract and normalize the text into the application’s documented return type.
13. Move the loading-only setting to model loading/configuration and pass only generation settings to generation.
14. Keep the application-level interface, input/output contract, fallback behavior, and tests stable.
15. It should accept structured messages or a prompt and return normalized text, with a safe error/fallback path.
