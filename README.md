## Purpose

This repository demonstrates a minimal CQRS-style architecture using plain Python and MongoDB.

It exists to show:

- how to separate write and read models

- how to make projections idempotent

- how to recover from corruption by replay

- how to bound and observe failure

No external infrastructure is required.

## Structure
```
src/
  app_baseline/     # naive CRUD version
  app_cqrs/         # CQRS version
  commands.py       # write model
  projector.py      # read model projection
  worker.py         # projection worker
  db.py             # Mongo connection
  metrics.py        # observability
  consistency.py    # consistency contract
  scripts/
    rebuild.py      # full replay
```

## Data Model
### Write model (`commands` collection)

Source of truth.

Fields:

- subject

- message

- status

- agent_note

- version (monotonic)

- updated_at

### Read model (`reads` collection)

Derived, disposable.

Fields:

- subject

- status

- preview

- has_note

- version

- schema_version

- updated_at

May be deleted and rebuilt at any time.

### Event Model (`events` collection)

Internal queue.

Fields:

- type

- ticket_id

- processed

- attempts

- error

Used only for:

- retry

- ordering

- observability

Not a domain log.

## Running Locally
```
docker compose up --build
```

API:

```
POST /tickets
PATCH /tickets/{id}/status
PATCH /tickets/{id}/note
GET /tickets/{id}
GET /metrics
```

## Worker

The worker is a deterministic poller:

- picks one unprocessed event

- runs projection

- marks processed

- retries up to MAX_ATTEMPTS

If it dies, nothing breaks.
If projections fail, backlog grows.
If backlog grows, metrics show it.

No hidden state.

## Replay / Recovery

To rebuild all read models:
```
python src/scripts/rebuild.py
```

This:

- deletes all read data

- reprojects from write model

- is safe to run multiple times

This is the primary operational guarantee of the system.

## Consistency Semantics

This system is:

- eventually consistent

- monotonic on writes

- idempotent on projections

Explicit contract:
```
READ_LAG_MS = 500
```

The system exposes its own consistency boundary.

No illusion of strong consistency.

## Failure Modes

Handled:

- duplicate events

- out-of-order events

- partial projections

- worker crashes

- corrupt read model

Not handled:

- network partitions

- multi-writer conflicts

- distributed transactions

- clock skew beyond seconds

Those require different system classes.

## Why This Exists

Most “CQRS” examples:

- hide failure

- assume perfect ordering

- cannot replay

- rely on infrastructure to fix design

This one forces all invariants into code:

- version monotonicity

- idempotency

- bounded retries

- measurable backlog

- explicit guarantees