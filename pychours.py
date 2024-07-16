from pychorus import find_and_output_chorus
from pychorus import create_chroma
from pychorus.similarity_matrix import TimeTimeSimilarityMatrix, TimeLagSimilarityMatrix




chorus_start_sec = find_and_output_chorus(
    r"C:\Users\pagug\Downloads\AIDJ\Victony - My Darling (Official Visualizer).mp3",
    r"C:\Users\pagug\Downloads\AIDJ\chorus_output.wav",
    clip_length=30
)
print(f"Chorus starts at: {chorus_start_sec} seconds")


# chroma, _, sr, _ = create_chroma( r"C:\Users\pagug\Downloads\AIDJ\Tems - Free Fall (Visualizer) ft. J. Cole.mp3")
# time_time_similarity = TimeTimeSimilarityMatrix(chroma, sr)
# time_lag_similarity = TimeLagSimilarityMatrix(chroma, sr)

# # Visualize the results
# time_time_similarity.display()
# time_lag_similarity.display()