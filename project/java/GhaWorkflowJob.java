package example;

/* metamodel_version: 1.12.0 */
/* version: 2026-10-28 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  A job under a workflow's `jobs` key: steps that run on a runner, or a call to a reusable workflow.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaWorkflowJob  {

  private String jobId;
  private String jobName;
  private String calls;
  private List<String> runsOn;
  private String runnerGroup;
  private String runnerEnvironment;
  private List<String> jobPermissions;


}