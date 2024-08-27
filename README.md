# Introduction
Essentially an implementation of [CS50][cs50]'s [Project 4][project4],
namely, a toy 𝕏-like social network.

![screenshot](https://github.com/mbivert/django-network/blob/master/screenshot.jpg?raw=true)

# TODO/BUGS

  - Form edition doesn't work without JS;
  - Forms's grid is fragile (okay on wide screen, messed up when shrinked);
  - An error case hidden from regular end-user is poorly managed (error not
  shown to user). It practically doesn't matter, but would be nice to find a
  clean way to solve it regardless;
  - When deleting items from the UI, not reloading the page also means we're
  not updating the pagination data: if we delete a few items, and then try
  to move to the last page, we might get an error because that page doesn't
  exist anymore (**post deletion wasn't part of the original spec**, probably
  for such reasons). Perhaps there's a way to tweak the pagination mechanism
  to redirect instead of failing.


[cs50]:     https://cs50.harvard.edu/web/2020/
[project4]: https://cs50.harvard.edu/web/2020/projects/4/network/
