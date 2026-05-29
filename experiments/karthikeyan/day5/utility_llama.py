import os
import json
import time
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv
from groq import Groq


# LOAD ENV VARIABLES
load_dotenv()


class GroqLlamaUtility:
    """Utility class for interacting with Groq Llama 3.1 8B Instant model."""
    
    def __init__(self, temperature: float = 0.7, json_output: bool = False):
        """
        Initialize the Groq Llama utility.
        
        Args:
            temperature: Temperature for model responses (0-2)
            json_output: Whether to output results as JSON
        """
        groq_key = os.getenv("GROQ_API_KEY")
        
        if not groq_key:
            raise ValueError("GROQ_API_KEY is missing in .env file")
        
        self.client = Groq(api_key=groq_key)
        self.model = "llama-3.1-8b-instant"
        self.temperature = temperature
        self.json_output = json_output
        self.conversation_history = []
        
    def call_llama(self, prompt: str) -> Dict[str, Any]:
        """
        Call Llama model with a single prompt.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Dictionary with response text and metadata
        """
        try:
            start_time = time.perf_counter()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature
            )
            
            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000
            
            result = {
                "prompt": prompt,
                "response": response.choices[0].message.content,
                "latency_ms": latency_ms,
                "model": self.model,
                "status": "success"
            }
            
            return result
            
        except Exception as e:
            return {
                "prompt": prompt,
                "response": None,
                "error": str(e),
                "model": self.model,
                "status": "error"
            }
    
    def chain_prompts(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """
        Chain multiple prompts where context flows from one to the next.
        
        Args:
            prompts: List of prompts to execute in sequence
            
        Returns:
            List of results from each prompt in the chain
        """
        results = []
        context = ""
        
        try:
            for i, prompt in enumerate(prompts):
                # Add context from previous response if available
                if i > 0 and results[-1]["status"] == "success":
                    context = results[-1]["response"]
                    full_prompt = f"Based on the following context:\n{context}\n\nNow: {prompt}"
                else:
                    full_prompt = prompt
                
                result = self.call_llama(full_prompt)
                result["chain_step"] = i + 1
                results.append(result)
                
        except Exception as e:
            results.append({
                "error": str(e),
                "status": "error",
                "chain_step": len(results) + 1
            })
        
        return results
    
    def output_results(self, results: Any, use_json: bool = None) -> str:
        """
        Format results for output.
        
        Args:
            results: Result(s) to output
            use_json: Override json_output setting
            
        Returns:
            Formatted output string
        """
        use_json = use_json if use_json is not None else self.json_output
        
        if use_json:
            if isinstance(results, list):
                return json.dumps(results, indent=2)
            else:
                return json.dumps(results, indent=2)
        else:
            if isinstance(results, list):
                output = []
                for i, result in enumerate(results, 1):
                    output.append(f"\n{'='*60}")
                    output.append(f"Chain Step {i}")
                    output.append(f"{'='*60}")
                    
                    if result.get("status") == "success":
                        output.append(f"Prompt: {result['prompt']}")
                        output.append(f"\nResponse:\n{result['response']}")
                        output.append(f"\nLatency: {result['latency_ms']:.2f} ms")
                    else:
                        output.append(f"Error: {result.get('error', 'Unknown error')}")
                
                return "\n".join(output)
            else:
                if results.get("status") == "success":
                    output = f"Prompt: {results['prompt']}\n"
                    output += f"Response:\n{results['response']}\n"
                    output += f"Latency: {results['latency_ms']:.2f} ms"
                    return output
                else:
                    return f"Error: {results.get('error', 'Unknown error')}"


def main():
    """Main entry point with argparse support."""
    parser = argparse.ArgumentParser(
        description="Groq Llama 3.1 8B Instant Utility - Execute prompts with prompt chaining support"
    )
    
    parser.add_argument(
        "--text",
        type=str,
        help="Single prompt to execute"
    )
    
    parser.add_argument(
        "--prompts",
        type=str,
        nargs="+",
        help="Multiple prompts for chain execution"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for model responses (0-2, default: 0.7)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Save output to a file"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize utility
        utility = GroqLlamaUtility(
            temperature=args.temperature,
            json_output=args.json
        )
        
        # Execute prompt(s)
        if args.text:
            # Single prompt
            results = utility.call_llama(args.text)
        elif args.prompts:
            # Chain of prompts
            results = utility.chain_prompts(args.prompts)
        else:
            # Default example
            results = utility.call_llama("Explain Artificial Intelligence in simple words.")
        
        # Format output
        output = utility.output_results(results)
        
        # Print output
        print(output)
        
        # Save to file if specified
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"\nOutput saved to {args.output}")
            
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
