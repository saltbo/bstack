# Delivery Engineering

Distinguish preparation, review, and deployment. Every deploy, a recovery
redeploy included, pauses for the user per saltmode Autonomy. After an
approved deploy, carry it through post-deployment regression.

- [Compatibility](compatibility.md): supported versions, persisted-data
  migrations, feature-flag transitions, rollback, and reproducible artifacts.
- [Deployment](deployment.md): local acceptance, target and artifact
  selection, provider execution, live regression, and recovery.

Establish BEP delivery conventions appropriate to the actual runtime. Honor the
project's support promise and API version policy. Improve unpublished behavior
directly where no supported consumer or persisted-data boundary requires
compatibility.

Read [production verification guidance](../production-verification/guide.md)
for post-deployment regression. Both modules are included in this bundle.
Report preparation, deployment, and regression outcomes distinctly.
