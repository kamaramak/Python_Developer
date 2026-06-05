from datetime import datetime


def distribute_donations(
    actual_donation,
    actual_project,
):
    if actual_project.invested_amount is None:
        actual_project.invested_amount = 0
    if actual_donation.invested_amount is None:
        actual_donation.invested_amount = 0

    project_money = (
        actual_project.full_amount - actual_project.invested_amount
    )
    donation_money = (
        actual_donation.full_amount - actual_donation.invested_amount
    )
    if donation_money >= project_money:
        actual_project.invested_amount += project_money
        actual_project.fully_invested = True
        actual_project.close_date = datetime.now()

        actual_donation.invested_amount += project_money
    else:
        actual_project.invested_amount += donation_money

        actual_donation.invested_amount = actual_donation.full_amount

    if actual_donation.full_amount == actual_donation.invested_amount:
        actual_donation.close_date = datetime.now()
        actual_donation.fully_invested = True
