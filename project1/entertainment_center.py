import media

toy_story = media.Movie("Toy Story", "A story about toys coming to life", "image", "trailerLink")

print(toy_story.storyline)

avatar = media.Movie("Avatar", "a marine on an alien planet", "avatar pic", "ahttps://www.youtube.com/watch?v=5PSNL1qE6VY")

print(avatar.storyline)

avatar.show_trailer()
