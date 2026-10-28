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
  A workflow file in a repository's `.github/workflows` directory: the events that run it, the access its GITHUB_TOKEN gets, and its jobs.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaWorkflow  {

  private List<String> triggers;
  private URI workflowUri;
  private String workflowPath;
  private URI workflowRepository;
  private List<String> permissions;
  private List<GhaWorkflowJob> jobs;


}