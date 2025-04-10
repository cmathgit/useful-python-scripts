import numpy as np
import hashlib

# Define a class for managing orthogonal prompt vectors
class OrthogonalPromptEngine:
    def __init__(self, dimensions=128):
        self.dimensions = dimensions
        self.trait_vectors = {}

    def vectorize_trait(self, trait):
        vec = np.zeros(self.dimensions, dtype=float)
        padded = f"^{trait}$"
        for i in range(len(padded) - 2):
            ngram = padded[i:i+3]
            h = int(hashlib.md5(ngram.encode()).hexdigest(), 16)
            idx = h % self.dimensions
            vec[idx] += 1
        normalized_vec = vec / np.linalg.norm(vec)
        return normalized_vec

    def add_trait(self, name, trait_description):
        if name in self.trait_vectors:
            raise ValueError(f"Trait '{name}' already exists.")
        vector = self.vectorize_trait(trait_description)
        self.trait_vectors[name] = vector

    def generate_prompt(self, selected_traits):
        prompt_vector = np.zeros(self.dimensions, dtype=float)
        for trait in selected_traits:
            if trait not in self.trait_vectors:
                raise ValueError(f"Trait '{trait}' not found.")
            prompt_vector += self.trait_vectors[trait]

        # Normalize prompt vector
        prompt_vector /= np.linalg.norm(prompt_vector)

        return prompt_vector

    def similarity(self, trait_a, trait_b):
        vec_a = self.trait_vectors.get(trait_a)
        vec_b = self.trait_vectors.get(trait_b)
        if vec_a is None or vec_b is None:
            raise ValueError("One or both traits not found.")
        return np.dot(vec_a, vec_b)


# Example Usage
if __name__ == "__main__":
    engine = OrthogonalPromptEngine(dimensions=256)

    # Add orthogonal traits
    engine.add_trait("melancholic", "deep sadness and reflective mood")
    engine.add_trait("hopeful", "optimistic resilience despite challenges")
    engine.add_trait("acoustic_style", "minimalist acoustic instrumentation")

    # Generate engineered prompt
    selected = ["melancholic", "hopeful", "acoustic_style"]
    prompt_vec = engine.generate_prompt(selected)

    print("Engineered Prompt Vector:", prompt_vec)

    # Check similarity between traits
    similarity_score = engine.similarity("melancholic", "hopeful")
    print(f"Similarity between 'melancholic' and 'hopeful': {similarity_score:.4f}")
