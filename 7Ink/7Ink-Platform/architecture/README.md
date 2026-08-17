# Architecture Notes

## Application boundaries

- Website: public pages and website-facing APIs
- Dashboard: authentication, staff workflows, and administrative APIs
- Platform: shared contracts and infrastructure material

Cross-application changes should define the contract in `7Ink-Platform` first, then update each consumer.
