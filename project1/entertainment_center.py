import media
import fresh_tomatoes

#create the movies
train_to_busan = media.Movie("Train To Busan", "While a zombie virus breaks out in South Korea, passengers struggle to survive on the train from Seoul to Busan.","https://a.ltrbxd.com/resized/sm/upload/y8/32/tq/s0/7ECxt8z3EM9jJmS4XErT5IgivnI-0-230-0-345-crop.jpg?k=3d055e706c","https://www.youtube.com/watch?v=pyWuHv2-Abk")
the_imitation_game = media.Movie("The Imitation Game", "During World War II, mathematician Alan Turing tries to crack the enigma code with help from fellow mathematicians.","https://images-na.ssl-images-amazon.com/images/M/MV5BOTgwMzFiMWYtZDhlNS00ODNkLWJiODAtZDVhNzgyNzJhYjQ4L2ltYWdlXkEyXkFqcGdeQXVyNzEzOTYxNTQ@._V1_UX182_CR0,0,182,268_AL_.jpg","https://www.youtube.com/watch?v=S5CjKEFb-sM")
rogue_one = media.Movie("Rogue One", "The Rebel Alliance makes a risky move to steal the plans for the Death Star, setting up the epic saga to follow.","https://images-na.ssl-images-amazon.com/images/M/MV5BMjEwMzMxODIzOV5BMl5BanBnXkFtZTgwNzg3OTAzMDI@._V1_UX182_CR0,0,182,268_AL_.jpg", "https://www.youtube.com/watch?v=frdj1zb9sMY")
v_for_vendetta = media.Movie("V For Vendetta", "In a future British tyranny, a shadowy freedom fighter, known only by the alias of 'V', plots to overthrow it with the help of a young woman.","https://timesofindia.indiatimes.com/img/57394290/Master.jpg", "https://www.youtube.com/watch?v=qxyUl9M_7vc")
zombieland = media.Movie("Zombieland", "A shy student trying to reach his family in Ohio, a gun-toting tough guy trying to find the last Twinkie, and a pair of sisters trying to get to an amusement park join forces to travel across a zombie-filled America.","http://www.sonypictures.com/movies/zombieland/assets/images/onesheet.jpg", "https://www.youtube.com/watch?v=8m9EVP8X7N8")
our_times = media.Movie("Our Times", "Love grows where it isn't expected in this endearing romantic comedy coming of age movie.", "https://upload.wikimedia.org/wikipedia/en/f/f3/Our_Times%2C_Movie_Poster.jpg","https://www.youtube.com/watch?v=ER61b0ejzlg")


movies = [train_to_busan, the_imitation_game, rogue_one, v_for_vendetta, zombieland, our_times]
fresh_tomatoes.open_movies_page(movies)
