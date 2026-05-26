# Week 1 Summary — GenAI Training

## Name
Karthikeyan

---

# 1. What I Learned

During Week 1, I learned the fundamentals of Generative AI engineering using Gemini 2.5 Flash and Python.

Key concepts learned:

- Gemini API integration using Python
- Prompt engineering basics
- Structured JSON generation
- Prompt refinement and iteration
- Vision-based prompting using images
- Batch processing workflows
- Command-line utility development
- Prompt chaining using sequential LLM calls
- Passing outputs between multiple Gemini calls
- API cost estimation and token understanding
- Rate limit concepts and retry strategies
- Testing and debugging GenAI utilities
- Utility design specification and workflow planning

I also learned how production-style GenAI systems are designed using modular workflows, chaining, testing, and operational analysis.

---

# 2. What I Built

## Day 1 Artifacts
- Gemini API setup
- Environment configuration using .env
- Basic Gemini text generation scripts
- Prompt experimentation utilities

---

## Day 2 Artifacts
- json_extractor_v2.py
- json_extractor_v3.py
- compare_prompts.py
- vision_test.py
- Prompt comparison outputs
- Image understanding workflows
- Structured JSON extraction utilities

Output files:
- json_extractor_output_v3.txt
- compare_prompts_output.txt
- findings2.md
- tracker_update.txt

---

## Day 3 Artifacts

### Core Utilities
- mini_utility.py
- mini_utility_v2.py
- batch_processor.py
- batch_processor_v2.py
- chained_utility.py

### Output Files
- mini_utility_output.txt
- mini_utility_v2_output.txt
- batch_processor_output.txt
- chained_utility_output.txt
- batch_results.json

### Documentation
- utility_spec.md
- cost_analysis.md
- testing_report.md
- day3_findings.md
- mini_utility_notes.md
- tracker_update.txt

### Testing Files
- utility_testoutput1.txt

---

# 3. What Is Still Unclear

Some topics I still want to understand more deeply:

- Advanced rate-limit handling strategies
- Streaming Gemini responses
- Async API workflows
- Token optimization techniques
- Production deployment architecture
- Memory systems and AI agents
- Long-context prompt management

---

# 4. What I’m Most Curious To Explore Further

I am most interested in learning:

- AI agents and autonomous workflows
- Multi-agent systems
- RAG (Retrieval-Augmented Generation)
- LangChain and orchestration frameworks
- Real-time AI applications
- Voice-based AI systems
- Production-scale GenAI architecture

I also want to explore how large companies design scalable GenAI systems with monitoring, caching, and distributed workflows.

---

# 5. What I Would Do Differently If I Redid Day 1

If I restarted Day 1, I would:

- Spend more time understanding prompt structure early
- Plan project workflows before coding
- Organize files more systematically from the beginning
- Focus earlier on structured outputs and error handling
- Document learnings continuously instead of later
- Understand Gemini model behavior more deeply before experimentation

I would also start testing edge cases earlier to improve debugging and reliability skills.

---

# Final Reflection

Week 1 helped me understand that GenAI engineering is not just about calling APIs. It involves workflow design, prompt engineering, chaining, testing, optimization, operational thinking, and scalable system design.

The most valuable learning for me was understanding prompt chaining and how multi-stage AI workflows are built using sequential LLM calls.