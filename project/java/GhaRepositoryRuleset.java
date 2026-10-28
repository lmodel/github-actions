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
  A ruleset: named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that it targets.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaRepositoryRuleset  {

  private URI rulesetUri;
  private Integer rulesetId;
  private String rulesetSourceType;
  private String rulesetSource;
  private String rulesetTarget;
  private String enforcement;
  private List<String> refNameInclude;
  private List<String> refNameExclude;
  private List<GhaBypassActor> bypassActors;
  private List<String> ruleTypes;
  private List<GhaRequiredStatusCheck> requiresCheck;


}