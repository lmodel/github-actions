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
  A status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context a check run must report.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaRequiredStatusCheck  {

  private URI checkUri;
  private String checkContext;
  private Integer integrationId;
  private Boolean strictPolicy;
  private Boolean doNotEnforceOnCreate;
  private List<String> jobPath;
  private List<String> skipConditions;
  private GhaWorkflow emittedBy;


}