import click

from .gh import GHContributions
from .utils import *


@click.command()
@click.argument("username")
@click.option("--today", is_flag=True, help="Today's contribution count.")
@click.option("--this-week", is_flag=True,
              help="This week's contribution count.")
@click.option("--this-year", is_flag=True,
              help="This year's contribution count.")
@click.option("--current-level", is_flag=True,
              help="Current level based on today's contribution count.")
@click.option("--next-level", is_flag=True,
              help="Minimum amount of contributions needed to level up.")
@click.option("--streak", is_flag=True, help="Streak of daily contributios.")
@click.option("--goal", type=int, help="Set your daily goal of contributions.")
def dontbs(username, today, this_week, this_year, current_level, next_level,
          streak, goal):
    if goal:
        set_gh_goal(goal)
        click.echo("GH Goal Set.")
        exit()

    contributions = GHContributions(username)

    def judge_contributions(c: int) -> None:
        goal = get_gh_goal()
        if c == 0:
            insult = generate_insult()
            click.echo(click.style("0 Contributions... wow", fg="red"))
            if goal > 0:
                click.echo(
                    click.style(
                        f"Let me remind your daily goal: {goal} Contributions",
                        fg="yellow"
                    )
                )
            click.echo(click.style(insult, fg="red"))
        else:
            click.echo(click.style(f"{c} Contributions", fg="green"))
            if goal < 1:
                return
            if c >= goal:
                click.echo(click.style("Daily goal reached!", fg="yellow"))
            else:
                click.echo(
                    click.style(
                        f"{goal-c} Contributions away from your daily goal",
                        fg="green"
                    )
                )

    if today:
        judge_contributions(contributions.today)

    if this_week:
        judge_contributions(contributions.this_week)

    if this_year:
        judge_contributions(contributions.this_year)

    if current_level:
        l = contributions.current_level
        if l == 0:
            insult = generate_insult()
            click.echo(click.style("Level 0", fg="red"))
            click.echo(click.style(insult, fg="red"))
        elif l == 4:
            click.echo(click.style("MAX LEVEL!", blink=True, bold=True, fg="yellow"))
            click.echo("Keep going tho")
        else:
            click.echo(click.style(f"Level {l}, not bad", fg="green"))
            c = contributions.to_level_up
            click.echo(
                click.style(
                    f"But you're {c} contributions away from level {l+1}",
                    fg="yellow"
                )
            )

    if next_level:
        c = contributions.to_level_up
        if c == 0:
            click.echo(click.style("MAX LEVEL!", blink=True, bold=True, fg="yellow"))
            click.echo("Keep going tho")
        else:
            nl = contributions.current_level + 1
            click.echo(f"{c} contributions away from level {nl}")

    if streak:
        s = contributions.streak
        if s == 0:
            click.echo(click.style(s, fg="red"))
        elif s > 0 and s < 10:
            click.echo(click.style(s, fg="green"))
        else:
            click.echo(click.style(s, fg="yellow"))
