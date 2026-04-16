# Sprint 1 Organization

## Main entities
- **User**: stores the basic information of the system user.
- **Membership**: stores the plan selected by the user.
- **Payment**: stores the payment made for a membership.

## Controllers
- **UserController**: validates the email, hashes the password and saves the user.
- **MembershipController**: validates the user and saves the selected membership.
- **PaymentController**: validates user, membership, ownership and payment amount before saving.

## Relationships
- One **User** can have many **Memberships**.
- One **Membership** can have many **Payments**.
- One **User** can make many **Payments**.

## Persistence
- Table `users`
- Table `memberships`
- Table `payments`

## Main flow
1. Register the user.
2. Assign a membership to the user.
3. Register the payment linked to the user and the membership.
