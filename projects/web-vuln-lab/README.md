# Web Vuln Lab: access control and repair verification

**Type:** existing software security project

**Stack:** Java 17, Spring Boot, Spring Security, Thymeleaf, PostgreSQL, Maven and JUnit

**Repository:** [web-vuln-lab-secure-remediation](https://github.com/HuLu338/web-vuln-lab-secure-remediation)

## Objective

Compare vulnerable and protected web behavior in one controlled application. The central case is object-level authorization: knowing a file identifier must not be enough to read someone else's file. A second case checks whether ordinary users can access an administrator's audit endpoint.

## Environment and tools

The repository uses a local Spring Boot application and PostgreSQL. Thymeleaf supplies the pages, while JUnit and MockMvc exercise the HTTP behavior. Demo users are selected through a request parameter. This is a learning shortcut and does not establish a trusted identity.

## Method

1. Read the repository setup instructions, configure a disposable local PostgreSQL database and start the application with the Maven Wrapper.
2. In the local demonstration, compare the vulnerable file route with the secure file route using a file owned by another demo user.
3. Trace the secure request from FileAccessService to AuthorizationService. The rule allows the owner or an administrator and denies a missing user or file.
4. Compare the vulnerable and secure administrator-audit routes with a regular user, then check the allowed administrator case.
5. Run the integration test class in the configured local environment. Check denial cases, legitimate access and audit events together; blocking every request would not be a correct repair.

These steps describe how to review the existing project. The portfolio refresh inspected the source and assertions; it did not rerun the application or claim a new passing test result.

## Results and evidence

The secure file service throws HTTP 403 when its ownership/admin policy fails. The vulnerable method loads the record by identifier without that check. The integration class contains seven test cases covering unauthorized file access, owner access, non-admin and admin access, and allowed/denied event logging.

| Evidence | What it supports |
|---|---|
| [AuthorizationService](https://github.com/HuLu338/web-vuln-lab-secure-remediation/blob/2f561e57c0d7defa48ea3a41fe4c16abfe213e57/src/main/java/web_vuln_lab/AuthorizationService.java) | Owner/admin policy and null checks |
| [FileAccessService](https://github.com/HuLu338/web-vuln-lab-secure-remediation/blob/2f561e57c0d7defa48ea3a41fe4c16abfe213e57/src/main/java/web_vuln_lab/FileAccessService.java) | Vulnerable lookup and guarded lookup with 403 denial |
| [AccessControlIntegrationTest](https://github.com/HuLu338/web-vuln-lab-secure-remediation/blob/2f561e57c0d7defa48ea3a41fe4c16abfe213e57/src/test/java/web_vuln_lab/AccessControlIntegrationTest.java) | Seven concrete regression scenarios and expected outcomes |
| [Vulnerability matrix](https://github.com/HuLu338/web-vuln-lab-secure-remediation/blob/2f561e57c0d7defa48ea3a41fe4c16abfe213e57/docs/vuln-matrix.md) | Access control, upload validation and stored-XSS case descriptions |

The wider project also demonstrates upload restrictions and escaped comment rendering. The illustration in this case study focuses only on the file-access policy above; it is not a live endpoint or newly captured test output.

## Reflection and next improvements

The useful AppSec pattern is to keep the insecure behavior, policy decision and regression assertion close enough to compare. It also matters to preserve access for the owner and administrator when adding a restriction.

The main limitation is identity handling. A user name in a request parameter can be changed by the caller. My next step is to replace that simulation with trusted session-based identity and repeat the same allowed/denied checks. I would also extend automated coverage for upload and XSS behavior. The vulnerable routes belong in a local teaching environment.

## Source and scope

This case study summarizes the existing public repository at commit `2f561e57c0d7defa48ea3a41fe4c16abfe213e57`, reviewed on 17 November 2026. Links are pinned to that snapshot. The portfolio adds explanation and a policy illustration; it does not claim production deployment, independent certification or a new test run.

[Return to the portfolio](../../index.html#projects)
